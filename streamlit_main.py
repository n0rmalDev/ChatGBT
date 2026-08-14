import os
import streamlit as st
import streamlit.components.v1 as components
import chromadb
from pypdf import PdfReader
from openai import OpenAI

# ------------------------------------------------------------------------------
# 1. Page Configuration & Tab Title Override
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="chatGBT",
    page_icon="😈",
    initial_sidebar_state="expanded"
)

components.html(
    """
    <script>
        window.parent.document.title = "chatGBT";
    </script>
    """,
    height=0,
    width=0,
)

# ------------------------------------------------------------------------------
# 2. Custom CSS: Pitch Black Theme, Purple Accents & Hidden Top Toolbar
# ------------------------------------------------------------------------------
st.markdown(
    """
    <style>
    header[data-testid="stHeader"] {
        visibility: hidden;
        height: 0%;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ------------------------------------------------------------------------------
# 3. Sidebar Knowledge Base Status
# ------------------------------------------------------------------------------
with st.sidebar:
    st.header("📄 Knowledge Base")
    st.caption("Attach a `.pdf` or `.txt` file directly in the chat box below!")

    if "pdf_filename" in st.session_state:
        st.success(f"Active Document: **{st.session_state.pdf_filename}**")
        if st.button("Clear Document Context"):
            del st.session_state.collection
            del st.session_state.pdf_filename
            st.rerun()
    else:
        st.info("No active document loaded.")

# ------------------------------------------------------------------------------
# 4. Main Chat App & API Setup
# ------------------------------------------------------------------------------
MODEL = "openrouter/free"

st.title("ChatGBT")
st.caption(f"Connected to OpenRouter: {MODEL}")

api_key = st.secrets.get("OPENROUTER_API_KEY", os.getenv("OPENROUTER_API_KEY"))

if not api_key:
    st.error("Please add OPENROUTER_API_KEY to Streamlit Secrets.")
    st.stop()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant. Always format LaTeX math equations using single dollar signs "
                "for inline math (e.g., $x^2$) and double dollar signs for block equations (e.g., $$x^2$$). "
                "Never use parentheses \\(...\\) or brackets \\[\\] for LaTeX."
            ),
        }
    ]

# Render chat history
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# ------------------------------------------------------------------------------
# 5. Handle Chat Input & Automatic File Attachment Processing
# ------------------------------------------------------------------------------
if prompt_data := st.chat_input("Ask a question or attach a file...", accept_file=True, file_type=["pdf", "txt"]):
    
    # Extract text and attached files
    if isinstance(prompt_data, str):
        user_text = prompt_data
        uploaded_files = []
    else:
        user_text = getattr(prompt_data, "text", "") or prompt_data.get("text", "")
        uploaded_files = getattr(prompt_data, "files", []) or prompt_data.get("files", [])

    # Process attached PDF / TXT file automatically if present
    if uploaded_files:
        for file in uploaded_files:
            with st.status(f"Reading & indexing {file.name}...", expanded=False) as status:
                text = ""
                if file.name.endswith(".pdf"):
                    reader = PdfReader(file)
                    for page in reader.pages:
                        extracted = page.extract_text()
                        if extracted:
                            text += extracted + "\n"
                elif file.name.endswith(".txt"):
                    text = file.read().decode("utf-8")

                # Sliding Window Chunking
                chunk_size, overlap = 300, 100
                step = chunk_size - overlap
                chunks = [
                    text[i : i + chunk_size]
                    for i in range(0, len(text), step)
                    if text[i : i + chunk_size].strip()
                ]

                # Index Chunks into ChromaDB
                chroma_client = chromadb.Client()
                try:
                    chroma_client.delete_collection("chat_docs")
                except Exception:
                    pass

                collection = chroma_client.create_collection("chat_docs")
                tags = [f"{file.name}_{i}" for i in range(len(chunks))]
                collection.add(documents=chunks, ids=tags)

                st.session_state.collection = collection
                st.session_state.pdf_filename = file.name
                status.update(label=f"Indexed {file.name} successfully!", state="complete")

    # Proceed with LLM completion if prompt text is submitted
    if user_text:
        with st.chat_message("user"):
            st.markdown(user_text)

        user_content = user_text
        if "collection" in st.session_state:
            results = st.session_state.collection.query(query_texts=[user_text], n_results=5)
            retrieved_docs = results["documents"][0] if results.get("documents") else []
            if retrieved_docs:
                context_str = "\n---\n".join(retrieved_docs)
                user_content = (
                    f"Use the following document context to answer the question.\n\n"
                    f"DOCUMENT CONTEXT:\n{context_str}\n\n"
                    f"USER QUESTION: {user_text}"
                )

        st.session_state.messages.append({"role": "user", "content": user_text})

        api_messages = [msg for msg in st.session_state.messages[:-1]]
        api_messages.append({"role": "user", "content": user_content})

        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""

            try:
                stream = client.chat.completions.create(
                    model=MODEL,
                    messages=api_messages,
                    stream=True,
                )

                for chunk in stream:
                    if chunk.choices and chunk.choices[0].delta.content:
                        full_response += chunk.choices[0].delta.content
                        response_placeholder.markdown(full_response + "▌")

                response_placeholder.markdown(full_response)
                st.session_state.messages.append({"role": "assistant", "content": full_response})

            except Exception as e:
                st.error(f"OpenRouter Error: {e}")