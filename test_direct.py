from backend.rag_service import RAGService
import sys

def main():
    print("Initializing RAGService...")
    try:
        service = RAGService()
        print("Service initialized.")
        
        query1 = "Tell me about OpenAI Codex."
        print(f"Querying Q1: {query1}")
        result1 = service.answer_query(query1)
        print("Result Q1:", result1)
        
        # Simulate history update
        from langchain_core.messages import HumanMessage, AIMessage
        history = [
            HumanMessage(content=query1),
            AIMessage(content=result1["answer"])
        ]
        
        query2 = "Describe its theme."
        print(f"Querying Q2: {query2}")
        result2 = service.answer_query(query2, history)
        print("Result Q2:", result2)
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
