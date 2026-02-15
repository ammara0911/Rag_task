import streamlit as st
import requests
import os

# Reads the backend API address from environment variables
API_URL = os.getenv("API_URL", "http://localhost:8000")

# setting page icon and title
st.set_page_config(page_title="RAG Chatbot", page_icon="🤖")
st.title("🤖 RAG Chatbot")

# Sidebar - File Upload
# letting the user to upload one or multiple files. only pdfs uploads
with st.sidebar:
    st.header("Document Upload")
    uploaded_files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)

    
    # user uploads the documents then he clicked the process domcuments, all files will be processed and disply success or error for each file
    if uploaded_files:
        if st.button("Process Documents"):
            for uploaded_file in uploaded_files:
                with st.spinner(f"Processing {uploaded_file.name}..."):
                    files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
                    try:
                        response = requests.post(f"{API_URL}/upload", files=files)
                        if response.status_code == 200:
                            st.success(f"Processed: {uploaded_file.name}")
                        else:
                            st.error(f"Error processing {uploaded_file.name}: {response.json()['detail']}")
                    except Exception as e:
                        st.error(f"Connection failed for {uploaded_file.name}: {e}")


# Initializes an in-memory list of chat messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input  and Sending to Backend
if prompt := st.chat_input("Ask a question about your documents..."):
    
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # sending user prompt to backend
                payload = {"query": prompt}
                response = requests.post(f"{API_URL}/chat", json=payload)

                # if success: displays generated answer, append answer to history and show sources.
                if response.status_code == 200:
                    data = response.json()
                    answer = data["answer"]
                    sources = data.get("sources", [])
                    
                    full_response = answer
                    if sources:
                        full_response += f"\n\n**Sources:** {', '.join(sources)}"
                    
                    st.markdown(full_response)
                    st.session_state.messages.append({"role": "assistant", "content": full_response})    
                else:
                    error_msg = f"Error: {response.json().get('detail', 'Unknown error')}"
                    st.error(error_msg)
            except Exception as e:
                st.error(f"Connection failed: {e}")
