import os
import streamlit as st
import streamlit.components.v1 as components
import chromadb
from pypdf import PdfReader
from openai import OpenAI

# 1. Page Configuration
st.set_page_config(
    page_title="chatGBT",
    page_icon="😈",
    initial_sidebar_state="expanded"  # Forces the sidebar to open on load
)

# Tab title override
components.html(
    """
    <script>
        window.parent.document.title = "chatGBT";
    </script>
    """,
    height=0,
    width=0,
)

# 2. Sidebar Setup (This creates the sidebar!)
with st.sidebar:
    st.header("📄 Knowledge Base")
    # 1. Update type to accept both pdf and txt extensions
    uploaded_file = st.file_uploader("Upload a PDF or TXT file", type=["pdf", "txt"])

    if uploaded_file and st.button("Process & Index File"):
        with st.spinner("Processing file..."):
            text = ""

            # 2. Extract text according to file extension
            if uploaded_file.name.endswith(".pdf"):
                reader = PdfReader(uploaded_file)
                for page in reader.pages:
                    extracted = page.extract_text()
                    if extracted:
                        text += extracted + "\n"

            elif uploaded_file.name.endswith(".txt"):
                # Read raw bytes and decode utf-8 plain text
                text = uploaded_file.read().decode("utf-8")

            # 3. Sliding window chunking (remains identical)
            chunk_size = 300
            overlap = 100
            step = chunk_size - overlap
            chunks = [
                text[i: i + chunk_size]
                for i in range(0, len(text), step)
                if text[i: i + chunk_size].strip()
            ]

            # 4. Store in ChromaDB
            chroma_client = chromadb.Client()
            try:
                chroma_client.delete_collection("chat_docs")
            except Exception:
                pass

            collection = chroma_client.create_collection("chat_docs")
            tags = [f"{uploaded_file.name}_{i}" for i in range(len(chunks))]
            collection.add(documents=chunks, ids=tags)

            st.session_state.collection = collection
            st.session_state.pdf_filename = uploaded_file.name
            st.success(f"Indexed {len(chunks)} chunks from {uploaded_file.name}!")


# 3. Main Chat App
MODEL = "openrouter/free"

st.title("ChatBot")
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

# 4. Handle Chat Input
if prompt := st.chat_input("Ask me anything..."):
    with st.chat_message("user"):
        st.markdown(prompt)

    user_content = prompt
    if "collection" in st.session_state:
        results = st.session_state.collection.query(query_texts=[prompt], n_results=5)
        retrieved_docs = results["documents"][0] if results.get("documents") else []
        if retrieved_docs:
            context_str = "\n---\n".join(retrieved_docs)
            user_content = (
                f"Use the following document context to answer the question.\n\n"
                f"DOCUMENT CONTEXT:\n{context_str}\n\n"
                f"USER QUESTION: {prompt}"
            )

    st.session_state.messages.append({"role": "user", "content": prompt})

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