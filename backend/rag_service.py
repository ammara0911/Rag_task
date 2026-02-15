import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

VECTOR_STORE_PATH = "faiss_index"

class RAGService:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        self.vector_store = self._load_vector_store()
        self.llm = ChatOpenAI(model="gpt-3.5-turbo") # or gpt-4

    def _load_vector_store(self):
        if os.path.exists(VECTOR_STORE_PATH):
            return FAISS.load_local(VECTOR_STORE_PATH, self.embeddings, allow_dangerous_deserialization=True)
        return None

    def add_document(self, text: str):
        # Split text
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        chunks = text_splitter.split_text(text)

        # Create or update vector store
        if self.vector_store is None:
            self.vector_store = FAISS.from_texts(chunks, self.embeddings)
        else:
            self.vector_store.add_texts(chunks)

        # Save locally
        self.vector_store.save_local(VECTOR_STORE_PATH)

    def get_retriever(self):
        if self.vector_store:
            return self.vector_store.as_retriever()
        return None

    def answer_query(self, query: str):
        if not self.vector_store:
            raise ValueError("Knowledge base is empty. Please upload a document first.")
            
        retriever = self.vector_store.as_retriever()
        
        prompt = ChatPromptTemplate.from_template("""
        Answer the following question based only on the provided context:

        <context>
        {context}
        </context>

        Question: {input}
        """)

        document_chain = create_stuff_documents_chain(self.llm, prompt)
        retrieval_chain = create_retrieval_chain(retriever, document_chain)
        
        response = retrieval_chain.invoke({"input": query})
        return response["answer"]
