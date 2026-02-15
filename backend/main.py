from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
import shutil
from backend.utils import process_pdf, save_upload_file_temp
from backend.rag_service import RAGService

app = FastAPI()
rag_service = RAGService()

@app.get("/")
async def root():
    return {"message": "RAG Chatbot API is running. Visit /docs for documentation."}

class QueryRequest(BaseModel):
    query: str
    session_id: str = "default_session"

# Simple in-memory history storage
chat_histories = {}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    Upload a PDF file, extract content, and add to vector store.
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")
    
    temp_file_path = save_upload_file_temp(file)
    
    try:
        result = process_pdf(temp_file_path)
        
        # Add to vector store with filename for source attribution
        rag_service.add_document(result["documents"], file.filename)
        
        return JSONResponse(content={
            "filename": file.filename,
            "num_pages": result["num_pages"],
            "message": "File processed and added to knowledge base successfully."
        })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
    finally:
        # Clean up the temp file
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

@app.post("/chat")
async def chat(request: QueryRequest):
    """
    Chat with the AI about the uploaded documents.
    """
    try:
        # Retrieve history
        session_history = chat_histories.get(request.session_id, [])
        
        # Get answer
        result = rag_service.answer_query(request.query, session_history)
        
        # Update history
        from langchain_core.messages import HumanMessage, AIMessage
        chat_histories.setdefault(request.session_id, []).extend([
            HumanMessage(content=request.query),
            AIMessage(content=result["answer"])
        ])
        
        return result
    except ValueError as e:
        # Handle case where knowledge base is empty
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating answer: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
