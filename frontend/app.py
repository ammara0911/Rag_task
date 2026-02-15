import streamlit as st
import requests
import os

# Configuration
API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="RAG Chatbot", page_icon="🤖")

st.title("🤖 RAG Chatbot")

# Sidebar - File Upload
with st.sidebar:
    st.header("Document Upload")
    uploaded_file = st.file_uploader("Upload a PDF", type="pdf")
    
    if uploaded_file is not None:
        if st.button("Process Document"):
            with st.spinner("Processing..."):
                files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
                try:
                    response = requests.post(f"{API_URL}/upload", files=files)
                    if response.status_code == 200:
                        st.success(f"Success! {response.json()['message']}")
                    else:
                        st.error(f"Error: {response.json()['detail']}")
                except Exception as e:
                    st.error(f"Connection failed: {e}")

# Main Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ask a question about your documents..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                payload = {"query": prompt}
                response = requests.post(f"{API_URL}/chat", json=payload)
                
                if response.status_code == 200:
                    answer = response.json()["answer"]
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    error_msg = f"Error: {response.json().get('detail', 'Unknown error')}"
                    st.error(error_msg)
            except Exception as e:
                st.error(f"Connection failed: {e}")
