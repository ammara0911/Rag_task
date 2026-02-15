# RAG Chatbot Application

## Project Overview
This is a Retrieval-Augmented Generation (RAG) Chatbot application built as a take-home assignment for an AI/ML Engineer role. It allows users to upload **multiple PDF documents**, processes them to extract text, indexes the content using FAISS, and enables users to chat with the documents using **Google's Gemini models**.

## Features
- **Multi-Document Ingestion**: Upload multiple PDF files via a simple UI.
- **Source Attribution**: The chatbot cites specific filenames for every answer.
- **RAG Architecture**: Uses LangChain and FAISS for efficient document retrieval.
- **Context-Aware Chat**: Remembers previous questions in a session to handle follow-ups (e.g., "Describe its theme").
- **Interactive Chat**: Chat interface powered by `gemini-flash-latest`.
- **Containerized**: Fully Dockerized for easy deployment.

## Tech Stack
- **Backend**: FastAPI
- **Frontend**: Streamlit
- **AI/ML**: LangChain, Gemini (Google Generative AI), FAISS
- **Containerization**: Docker, Docker Compose

## Setup Instructions

### Prerequisites
- Python 3.9+
- Docker & Docker Compose
- Google Gemini API Key

### Local Installation
1.  **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd <project_directory>
    ```

2.  **Environment Setup**:
    Copy `.env.example` to `.env` and add your Google API Key:
    ```bash
    cp .env.example .env
    # Edit .env and set GOOGLE_API_KEY
    ```

3.  **Install Dependencies**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: .\venv\Scripts\activate
    pip install -r requirements.txt
    ```

4.  **Run Locally**:
    - Backend: `uvicorn backend.main:app --reload`
    - Frontend: `streamlit run frontend/app.py`

## Docker Instructions
To run the entire application using Docker:

1.  Ensure Docker Desktop is running.
2.  Build and run the containers:
    ```bash
    docker-compose up --build
    ```
3.  Access the application:
    - **User Interface (Frontend)**: [http://localhost:8501](http://localhost:8501) <- **Use this to chat!**
    - **API Backend**: [http://localhost:8000](http://localhost:8000) (Now shows a welcome message)
    - **Interactive API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

## API Documentation

### `POST /upload`
Uploads a PDF file and adds it to the knowledge base.
- **Body**: `multipart/form-data` with `file` field.
- **Response**:
  ```json
  {
    "filename": "document.pdf",
    "num_pages": 10,
    "message": "File processed and added to knowledge base successfully."
  }
  ```

### `POST /chat`
Asks a question based on the uploaded documents.
- **Body**: JSON
  ```json
  {
    "query": "What is the main topic of the document?",
    "session_id": "optional-session-id"
  }
  ```
- **Response**:
  ```json
  {
    "answer": "The document discusses...",
    "sources": ["document.pdf"]
  }
  ```

## Architecture
1.  **Text Extraction**: `PyPDFLoader` is used to load PDFs as `Document` objects, preserving metadata.
2.  **Chunking**: `RecursiveCharacterTextSplitter` breaks text into smaller chunks (1000 chars) for efficient embedding.
3.  **Embeddings**: `GoogleGenerativeAIEmbeddings` (`models/gemini-embedding-001`) transforms text chunks into vector representations.
4.  **Vector Store**: `FAISS` indexes these vectors for fast similarity search.
5.  **Retrieval & Generation**:
    - The query is embedded.
    - Relevant text chunks are retrieved from FAISS.
    - `ChatGoogleGenerativeAI` (`gemini-1.5-flash`) generates an answer citing the sources.
