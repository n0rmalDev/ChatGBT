# 😈 chatGBT: AI Chatbot with Built-in RAG

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.38%2B-FF4B4B.svg)](https://streamlit.io/)
[![ChromaDB](https://img.shields.io/badge/Vector%20DB-ChromaDB-orange.svg)](https://www.trychroma.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**chatGBT** is a full-featured conversational AI web interface built with **Streamlit**, **OpenRouter**, and **ChromaDB**. It features a modern black theme with purple accents, native LaTeX mathematical formatting, and a seamless **Retrieval-Augmented Generation (RAG)** system. Users can attach PDF or TXT documents directly within the chat bar to ground responses in custom document context without extra manual steps.

---

## ✨ Features

- **📄 Native Inline RAG:** Drag and drop `.pdf` or `.txt` files directly in the chat input. Files are automatically indexed into ChromaDB with zero friction.
- **⚡ Sliding-Window Vector Search:** Custom chunking algorithm (`chunk_size = 300`, `overlap = 100`) with ChromaDB vector similarity queries (`n_results = 5`) for precise document retrieval.
- **🎨 Custom Pitch Black & Purple Theme:** Sleek, distraction-free UI with custom styling via `.streamlit/config.toml` and CSS overrides.
- **📐 Native LaTeX Math Rendering:** Configured with smart prompt formatting for inline (`$x^2$`) and block (`$$x^2$$`) LaTeX equations.
- **⚡ Real-Time Response Streaming:** Powered by OpenRouter's free and paid LLM options via the OpenAI Python SDK wrapper.
- **🧹 Session Memory Management:** Clear document context or full chat history directly from the sidebar with a single click.

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Frontend / Framework** | [Streamlit](https://streamlit.io/) — Rapid Python web UI |
| **Vector Database** | [ChromaDB](https://www.trychroma.com/) — Lightweight vector storage & retrieval |
| **PDF Processing** | [PyPDF](https://pypdf.readthedocs.io/) — Pure Python PDF text extraction |
| **LLM API** | [OpenRouter](https://openrouter.ai/) — Unified API for 100+ LLM models (free & paid) |
| **Language** | Python 3.10+ |

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+** installed on your system
- **Git** for cloning the repository
- **OpenRouter API Key** (free tier available at [openrouter.ai](https://openrouter.ai))

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/n0rmalDev/ChatGBT.git
   cd chatGBT
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your OpenRouter API key:**
   ```bash
   mkdir -p .streamlit
   ```
   
   Create `.streamlit/secrets.toml` with your API key:
   ```toml
   OPENROUTER_API_KEY = "your-openrouter-api-key-here"
   ```
   
   > **Get your API key:** Sign up for free at [openrouter.ai](https://openrouter.ai), then find your key in Settings → API Keys.

5. **Run the app:**
   ```bash
   streamlit run streamlit_main.py
   ```
   
   The app will open in your browser at `http://localhost:8501`.

---

## 📖 How It Works

### RAG Pipeline

1. **Document Upload:** User attaches a PDF or TXT file via the chat input
2. **Text Extraction:** PyPDF extracts raw text from PDFs; TXT files are read directly
3. **Chunking:** Text is split into overlapping chunks (300 chars, 100 char overlap) for semantic coherence
4. **Vector Indexing:** Chunks are embedded and stored in ChromaDB's in-memory collection
5. **Retrieval:** User query is vectorized and matched against stored chunks (`n_results=5`)
6. **Context Injection:** Top matches are prepended to the user message as system context
7. **LLM Response:** OpenRouter processes the augmented prompt and streams the response

### Session State Management

- **Chat History:** All messages are stored in `st.session_state.messages` (includes system prompt)
- **Active Document:** ChromaDB collection persists in `st.session_state.collection` until manually cleared
- **Memory:** Clear document or chat directly from the sidebar without restarting the app

---

## 💡 Usage Tips

### Uploading Documents

- Click the chat input box and select a file, or drag & drop directly
- Supported formats: `.pdf`, `.txt`
- Large PDFs may take a few seconds to index

### Asking Questions

- Ask natural language questions; the RAG system will automatically search uploaded documents
- Without a document, chatGBT behaves as a standard conversational AI
- Math equations are rendered natively (e.g., `$E=mc^2$` or `$$\sum_{i=1}^{n} i = \frac{n(n+1)}{2}$$`)

### Managing Context

- **Clear Document:** Click "Clear Document Context" to remove the current RAG index
- **New Chat:** Reload the page to start a fresh conversation (preserves document)
- **Full Reset:** Click "Clear Document Context" + reload for a complete reset

---

## 🔧 Configuration

### Customizing the RAG Pipeline

Edit these values in `streamlit_main.py`:

```python
chunk_size = 300      # Characters per chunk
overlap = 100         # Character overlap between chunks
n_results = 5         # Number of retrieved documents to send to LLM
MODEL = "openrouter/free"  # Switch to paid model: "openrouter/auto"
```

### Theming

Modify `.streamlit/config.toml` for dark/light mode and colors:

```toml
[theme]
primaryColor = "#9d4edd"
backgroundColor = "#0d0d0d"
secondaryBackgroundColor = "#1a1a1a"
textColor = "#ffffff"
```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| **API Key Error** | Ensure `.streamlit/secrets.toml` exists with valid `OPENROUTER_API_KEY` |
| **PDF not extracting text** | PDFs with scanned images (not embedded text) won't extract; OCR not supported |
| **Slow responses** | OpenRouter free tier has rate limits; upgrade to paid or wait between requests |
| **Math not rendering** | Ensure LaTeX is wrapped in `$...$` (inline) or `$$...$$` (block) |
| **Virtual environment issues** | Try `python -m venv venv` and ensure you're in the activated environment |

---

## 📝 Project Structure

```
chatGBT/
├── streamlit_main.py      # Main application logic
├── requirements.txt       # Python dependencies
├── .streamlit/
│   ├── config.toml        # UI theme & settings
│   └── secrets.toml       # API keys (DO NOT commit)
├── README.md              # This file
└── LICENSE                # MIT License
```

---

## 📜 License

Distributed under the MIT License. See [LICENSE](LICENSE) for more information.

---

## 🤝 Contributing

Contributions are welcome! Feel free to:

- Report bugs or request features via GitHub Issues
- Submit pull requests with improvements
- Share feedback and suggestions

---

## ⚠️ Important Notes

- **API Costs:** OpenRouter free tier is rate-limited. Monitor usage to avoid overages on paid plans.
- **Privacy:** Document content is processed locally (ChromaDB runs in-memory) but sent to OpenRouter for LLM processing.
- **Session Persistence:** Chat history and documents are cleared on page reload (not persistent).

---

**Questions?** Open an issue on GitHub or check [OpenRouter Documentation](https://openrouter.ai/docs).
