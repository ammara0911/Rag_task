from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import os
import shutil
from .utils import process_pdf, save_upload_file_temp
from .rag_service import RAGService

app = FastAPI()
rag_service = RAGService()

class QueryRequest(BaseModel):
    query: str

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
        
        # Add to vector store
        rag_service.add_document(result["text"])
        
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
        answer = rag_service.answer_query(request.query)
        return {"answer": answer}
    except ValueError as e:
        # Handle case where knowledge base is empty
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating answer: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
