
# importing libraries
import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS
from langchain.chains import create_retrieval_chain, create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from dotenv import load_dotenv

# loading environment variables from .env file
load_dotenv()



VECTOR_STORE_PATH = "faiss_index"

class RAGService:
    def __init__(self):
        # Ensure GOOGLE_API_KEY is in environment

        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
        self.vector_store = self._load_vector_store()
        self.llm = ChatGoogleGenerativeAI(model="gemini-flash-latest")

    # Load or Initialize Vector Store.............
    def _load_vector_store(self):
        if os.path.exists(VECTOR_STORE_PATH):
            return FAISS.load_local(VECTOR_STORE_PATH, self.embeddings, allow_dangerous_deserialization=True)
        return None

    # Adding Documents to the Index................
    def add_document(self, documents, filename: str):
        
        # Update metadata to use a clean filename instead of full temp path
        for doc in documents:
            doc.metadata["source"] = filename

        # Split documents
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        chunks = text_splitter.split_documents(documents)

        # Create or update vector store
        if self.vector_store is None:
            self.vector_store = FAISS.from_documents(chunks, self.embeddings)
        else:
            self.vector_store.add_documents(chunks)

        # Save locally
        self.vector_store.save_local(VECTOR_STORE_PATH)


    # retries the vector store data
    def get_retriever(self):
        if self.vector_store:
            return self.vector_store.as_retriever()
        return None

    
    def answer_query(self, query: str, chat_history: list = []):

        # if no documents have been uploaded then raise an error
        if not self.vector_store:
            raise ValueError("Knowledge base is empty. Please upload a document first.")

        
        # Retrieves top 5 relevant text chunks per query    
        retriever = self.vector_store.as_retriever(search_kwargs={"k": 5})
        
        # Contextualize question prompt
        contextualize_q_system_prompt = """Given a chat history and the latest user question 
        which might reference context in the chat history, formulate a standalone question 
        which can be understood without the chat history. Do NOT answer the question, 
        just reformulate it if needed and otherwise return it as is."""
        contextualize_q_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", contextualize_q_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )

        # history-aware retrieval
        history_aware_retriever = create_history_aware_retriever(
            self.llm, retriever, contextualize_q_prompt
        )

        # Answer prompt, telling llm how to behave.
        qa_system_prompt = """You are an assistant for question-answering tasks. 
        Use the following pieces of retrieved context to answer the question. 
        If you don't know the answer, just say that you don't know. 
        Use three sentences maximum and keep the answer concise.
        Always cite the source filename in your answer.

        <context>
        {context}
        </context>"""
        
        qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", qa_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )

        #Building the Chains

        #Combines LLM + prompt template to generate answer using retrieved docs
        question_answer_chain = create_stuff_documents_chain(self.llm, qa_prompt)
        
        #Combines retriever + answer chain
        rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

        # running the chain
        response = rag_chain.invoke({"input": query, "chat_history": chat_history})


        
        # Extract unique sources
        sources = list(set([doc.metadata.get("source", "Unknown") for doc in response["context"]]))
        
        return {
            "answer": response["answer"],
            "sources": sources
        }
