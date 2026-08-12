import os
import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="chatGBT",
    page_icon="😈",  # Optional: sets a custom emoji favicon
)

# OpenRouter free model tag
MODEL = "openrouter/free"

st.title("ChatBot")
st.caption(f"Connected to OpenRouter: {MODEL}")

# Retrieve API key from Streamlit secrets or environment
api_key = st.secrets.get("OPENROUTER_API_KEY", os.getenv("OPENROUTER_API_KEY"))

if not api_key:
    st.error("Please add OPENROUTER_API_KEY to Streamlit Secrets.")
    st.stop()

# Point OpenAI client to OpenRouter's endpoint
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

# System prompt instructs the AI to use Streamlit-compatible LaTeX ($...$)
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

# Display message history (skipping the hidden system instruction)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Handle prompt input
if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""

        try:
            stream = client.chat.completions.create(
                model=MODEL,
                messages=st.session_state.messages,
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