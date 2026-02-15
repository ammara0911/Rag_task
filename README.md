# 🤖 RAG Chatbot with Context Awareness

A powerful Retrieval-Augmented Generation (RAG) chatbot that allows you to **chat with your PDF documents**. It features **context-aware conversations**, meaning it remembers what you asked previously to understand follow-up questions (e.g., "Describe its theme" after asking about a specific topic).

Built with **FastAPI**, **LangChain**, **Google Gemini**, and **Streamlit**. Fully Dockerized for easy deployment.

---

## 🚀 Key Features

*   **🧠 Context-Aware Memory**: The bot understands conversation history. If you ask "Who is the CEO?", and then "How old is he?", it knows "he" refers to the CEO.
*   **📚 Multi-Document Support**: Upload multiple PDF files to build a comprehensive knowledge base.
*   **🔍 Accurate Citations**: Every response includes the source filename so you know exactly where the information came from.
*   **⚡ Powered by Gemini**: Uses Google's latest `gemini-flash-latest` model for fast and high-quality responses.
*   **🐳 Dockerized**: Run the entire stack (Frontend + Backend) with a single command.

---

## 🛠️ Tech Stack

*   **Backend**: FastAPI (Python)
*   **Frontend**: Streamlit
*   **AI Orchestration**: LangChain
*   **Vector Store**: FAISS (Facebook AI Similarity Search)
*   **LLM**: Google Gemini (`gemini-flash-latest`)
*   **Embeddings**: Google Generative AI Embeddings (`models/gemini-embedding-001`)

---

## 🏁 Getting Started

### Prerequisites

*   **Docker Desktop** installed and running.
*   A **Google Gemini API Key** (Get it [here](https://aistudio.google.com/app/apikey)).

### Option 1: Run with Docker (Recommended)

This is the easiest way to run the application.

1.  **Clone the repository**:
    ```bash
    git clone https://github.com/ammara0911/Rag_task.git
    cd Rag_task
    ```

2.  **Set up Environment Variables**:
    Create a `.env` file in the root directory and add your API Key:
    ```bash
    GOOGLE_API_KEY=your_actual_api_key_here
    ```

3.  **Build and Run**:
    ```bash
    docker-compose up --build
    ```

4.  **Access the App**:
    *   **Frontend (Chat Interface)**: [http://localhost:8501](http://localhost:8501)
    *   **Backend API**: [http://localhost:8000](http://localhost:8000)
    *   **API Documentation (Swagger UI)**: [http://localhost:8000/docs](http://localhost:8000/docs)

---

### Option 2: Run Locally (For Development)

If you prefer running without Docker:

1.  **Create a Virtual Environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: .\venv\Scripts\activate
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Backend**:
    ```bash
    uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
    ```

4.  **Run the Frontend**:
    Open a new terminal, activate the venv, and run:
    ```bash
    streamlit run frontend/app.py
    ```

---

## 📖 API Documentation

The backend provides RESTful endpoints to interact with the system programmatically.

### 1. Upload Document
**Endpoint**: `POST /upload`  
**Description**: Uploads a PDF file, processes it, and indexes it into the vector store.

**Curl Example**:
```bash
curl -X POST "http://localhost:8000/upload" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@/path/to/your/document.pdf"
```

**Response**:
```json
{
  "filename": "document.pdf",
  "num_pages": 15,
  "message": "File processed and added to knowledge base successfully."
}
```

### 2. Chat with Context
**Endpoint**: `POST /chat`  
**Description**: Ask questions about the uploaded documents. Supports `session_id` to maintain conversation history.

**Curl Example**:
```bash
curl -X POST "http://localhost:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{
           "query": "What is the main conclusion?",
           "session_id": "user-session-123"
         }'
```

**Response**:
```json
{
  "answer": "The main conclusion of the document is...",
  "sources": ["document.pdf"]
}
```

---

## 🏗️ Architecture Flow

1.  **Ingestion**: User uploads a PDF.
2.  **Processing**: The system splits the text into chunks (1000 characters).
3.  **Embedding**: Chunks are converted into vectors using `gemini-embedding-001`.
4.  **Storage**: Vectors are stored in a local FAISS index.
5.  **Retrieval**:
    *   When a user asks a question, the system first checks the **chat history**.
    *   It reformulates the question to be standalone (e.g., "Describe its theme" -> "Describe the theme of Codex").
    *   It searches FAISS for the most relevant text chunks.
6.  **Generation**: The LLM (`gemini-flash-latest`) generates an answer using the retrieved chunks + the chat history.

---

## 📂 Project Structure

```
Rag_task/
├── backend/
│   ├── main.py          # FastAPI application & endpoints
│   ├── rag_service.py   # Core logic for RAG and LangChain
│   └── utils.py         # PDF processing utilities
├── frontend/
│   └── app.py           # Streamlit UI
├── Dockerfile           # Docker configuration
├── docker-compose.yml   # Container orchestration
├── requirements.txt     # Python dependencies
└── README.md            # Documentation
```
