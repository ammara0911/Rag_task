import os
import shutil
import tempfile
from langchain_community.document_loaders import PyPDFLoader

def process_pdf(file_path: str):
    """
    Process a PDF file and return its text content and page count.
    
    Args:
        file_path (str): Path to the PDF file.
        
    Returns:
        dict: A dictionary containing 'text' (str) and 'num_pages' (int).
    """
    loader = PyPDFLoader(file_path)
    pages = loader.load()
    
    text = ""
    for page in pages:
        text += page.page_content + "\n"
        
    # Basic cleaning
    cleaned_text = text.replace("\x00", "") 
    
    return {
        "text": cleaned_text,
        "num_pages": len(pages)
    }

def save_upload_file_temp(upload_file) -> str:
    """
    Save an uploaded file to a temporary file and return the path.
    """
    try:
        suffix = os.path.splitext(upload_file.filename)[1]
        # Create a temp file. delete=False to keep it for processing.
        # User is responsible for cleanup if needed, or we rely on OS temp cleaning.
        # In this flow, we might want to clean up after processing in the route.
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            shutil.copyfileobj(upload_file.file, tmp)
            tmp_path = tmp.name
        return tmp_path
    finally:
        upload_file.file.close()
