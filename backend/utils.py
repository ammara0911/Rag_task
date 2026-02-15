import os
import shutil
import tempfile
from langchain_community.document_loaders import PyPDFLoader



# Extracts and returns cleaned text page documents from a PDF file along with the total page count, preparing it for embedding and indexing.
def process_pdf(file_path: str):
    """
    Process a PDF file and return its document objects and page count.
    
    Args:
        file_path (str): Path to the PDF file.
        
    Returns:
        dict: A dictionary containing 'documents' (list) and 'num_pages' (int).
    """
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    
    # Null characters can cause issues in vector stores/LLMs
    for doc in documents:
        doc.page_content = doc.page_content.replace("\x00", "")
    
    return {
        "documents": documents,
        "num_pages": len(documents)
    }



# Saves an uploaded file to a named temporary file on disk and returns its path for further processing by loaders like the PDF extractor.
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
