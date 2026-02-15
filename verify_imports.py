try:
    import fastapi
    import uvicorn
    import streamlit
    import langchain
    import faiss
    import pypdf
    import dotenv
    import langchain_openai
    print("Imports successful")
except ImportError as e:
    print(f"Import failed: {e}")
    exit(1)
