# 😈 chatGBT: AI Chatbot with Built-in RAG

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.38%2B-FF4B4B.svg)](https://streamlit.io/)
[![ChromaDB](https://img.shields.io/badge/Vector%20DB-ChromaDB-orange.svg)](https://www.trychroma.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**chatGBT** is a full-featured conversational AI web interface built with **Streamlit**, **OpenRouter**, and **ChromaDB**. It features a modern black theme with purple accents, native LaTeX mathematical formatting, and a seamless **Retrieval-Augmented Generation (RAG)** system. Users can attach PDF or TXT documents directly within the chat bar to ground responses in custom document context without extra manual steps.

---

## ✨ Features

- **📄 Native Inline RAG:** Drag and drop `.pdf` or `.txt` files directly inside the chat bar (`st.chat_input`) or via the sidebar. Files are indexed into ChromaDB automatically.
- **⚡ Sliding-Window Vector Search:** Custom chunking algorithm (`chunk_size = 300`, `overlap = 100`) coupled with ChromaDB vector similarity queries (`n_results = 5`).
- **🎨 Custom Pitch Black & Purple Theme:** Custom UI styling configured via `.streamlit/config.toml` and CSS overrides.
- **📐 Clean LaTeX Math Rendering:** Configured with strict system prompt formatting rules for both inline (`$x^2$`) and block (`$$x^2$$`) LaTeX equations.
- **⚡ Real-Time Response Streaming:** Powered by OpenRouter streaming completions via the OpenAI Python SDK wrapper.
- **🧹 Memory & Context Management:** Easily clear active document context or chat sessions directly from the sidebar.

---

## 🛠️ Tech Stack

- **Frontend / Framework:** [Streamlit](https://streamlit.io/)
- **Vector Database:** [ChromaDB](https://www.trychroma.com/)
- **PDF Parser:** [PyPDF](https://pypdf.readthedocs.io/)
- **LLM API Provider:** [OpenRouter](https://openrouter.ai/) (via standard `openai` SDK)
- **Language:** Python 3.10+

---

## 📁 Repository Structure

```text
├── .streamlit/
│   └── config.toml          # Custom theme configuration (Dark mode & Purple accents)
├── streamlit_main.py        # Core application entry point
├── requirements.txt         # Dependencies list for local & cloud deployment
├── README.md                # Project documentation
└── .gitignore               # Ignores local secrets and python build caches
