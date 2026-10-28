# 🌌 AstroAI — AI-Powered Astronomy Assistant

**Explore the universe with AI.** 🚀

AstroAI is an AI-powered astronomy assistant designed to help users explore space, understand astronomical concepts, and learn about the universe through conversational AI.

Built with Python and Streamlit, AstroAI integrates Google's Gemini model for AI-powered conversations and supports a locally running Ollama model for private, offline-capable experimentation.

## ✨ Features

- 🤖 **AI-Powered Chat:** Ask questions about astronomy, planets, stars, galaxies, black holes, and more.
- 🌠 **Google Gemini Integration:** Get AI-generated explanations through the Gemini API.
- 💻 **Local Ollama Support:** Run a local language model on your own computer.
- 📚 **Knowledge Mode (RAG):** Retrieve relevant information from a custom astronomy knowledge base before generating an answer.
- 💬 **Chat History:** Keep track of your recent conversations.
- 🔭 **Astronomy Topic Suggestions:** Explore topics such as planets, stars, black holes, and galaxies.
- 🎨 **Space-Themed Interface:** A dark, cosmic-inspired interface built with Streamlit.

## 🛠️ Tech Stack

| Technology        | Purpose                                                       |
| ----------------- | ------------------------------------------------------------- |
| Python            | Core application logic                                        |
| Streamlit         | Interactive web interface                                     |
| Google Gemini API | Cloud-based AI responses                                      |
| Ollama            | Running local language models                                 |
| NumPy             | Similarity calculations for retrieval                         |
| Requests          | API communication                                             |
| Python-dotenv     | Loading environment variables                                 |
| RAG               | Retrieving relevant knowledge from a custom astronomy dataset |

## 🚀 Live Demo

**Try AstroAI:** [Open the Live App](https://astroai-j6hqrrpxzerv6nolemdba9.streamlit.app/)

> The live deployment currently uses Google Gemini. Local Ollama integration and Knowledge Mode are intended for local use while cloud compatibility is being improved.

## 💻 Run AstroAI Locally

### 1. Clone the repository

```bash
git clone https://github.com/vineyvarmavv4095818/AstroAI.git
cd AstroAI
```

Replace `vineyvarmavv4095818` with your GitHub username.

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Configure the Gemini API key

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Get an API key from [Google AI Studio](https://aistudio.google.com/).

**Important:** Never upload your `.env` file or expose your API key on GitHub.

### 5. Run the application

```bash
streamlit run streamlit_app.py
```

Streamlit will provide a local URL, usually `http://localhost:8501`.

## 🦙 Using Ollama Locally

AstroAI also supports local AI inference using Ollama.

1. Install [Ollama](https://ollama.com/).
2. Start Ollama on your computer.
3. Download the models used by your application.

For example:

```bash
ollama pull gemma3:1b
ollama pull nomic-embed-text
```

4. Run AstroAI locally and select Ollama where supported by the application.

- `gemma3:1b` is used for local AI conversations.
- `nomic-embed-text` is used to generate embeddings for Knowledge Mode.

**Note:** Ollama must be running on your computer. The local Ollama integration is not currently available in the live cloud deployment.

## 📚 Knowledge Mode — RAG

AstroAI includes an experimental Retrieval-Augmented Generation (RAG) workflow for astronomy-related questions.

The workflow:

1. Loads information from `space_knowledge.txt`.
2. Splits the knowledge base into smaller sections.
3. Generates embeddings using a local embedding model.
4. Retrieves relevant sections based on similarity to the user's question.
5. Uses the retrieved context to generate an answer.

This approach helps the assistant use relevant information from a custom knowledge base when answering questions.

## 📁 Project Structure

```text
AstroAI/
├── streamlit_app.py       # Streamlit user interface
├── app.py                 # AI model and application logic
├── space_knowledge.txt    # Custom astronomy knowledge base
├── requirements.txt       # Python dependencies
├── .gitignore             # Files excluded from Git
└── README.md              # Project documentation
```

## 🔐 Security Notes

- Keep API keys and credentials private.
- Store secrets in `.env` locally or Streamlit Secrets in the cloud.
- Never commit `.env`, virtual environments, or secret configuration files.
- Local Ollama endpoints should not be exposed publicly without appropriate authentication and security controls.

## 🗺️ Future Improvements

- [ ] Enable secure Ollama integration in the cloud deployment.
- [ ] Improve the astronomy knowledge base and retrieval accuracy.
- [ ] Add more astronomy learning resources.
- [ ] Improve response quality and error handling.
- [ ] Enhance the user interface and accessibility.

## 🎯 Project Goal

The goal of AstroAI is to make astronomy easier to explore through conversational AI, combining cloud-based language models with local AI experimentation and retrieval-based knowledge.

## 👨‍💻 Author

**Vinay Verma**

Computer Science & Engineering | AI/ML Enthusiast

---

⭐ If you find AstroAI interesting, consider starring the repository!
