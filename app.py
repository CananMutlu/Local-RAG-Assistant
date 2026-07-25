import streamlit as st
import os
from io import BytesIO
from src.database import init_db, clear_db
from src.ingestion import ingest_document
from src.rag_pipeline import answer_query

# Configure page
st.set_page_config(page_title="Local RAG Assistant", page_icon="🤖", layout="wide")

# Custom CSS for premium UI
st.markdown("""
<style>
    /* Dark mode premium theme */
    .stApp {
        background-color: #121212;
        color: #E0E0E0;
    }
    
    .stSidebar {
        background-color: #1E1E1E !important;
        border-right: 1px solid #333;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #FFFFFF !important;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
    }
    
    /* Title with gradient */
    .premium-title {
        background: linear-gradient(90deg, #bb86fc, #03dac6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    /* Chat bubbles */
    .user-msg {
        background-color: #bb86fc;
        color: #000000;
        padding: 15px;
        border-radius: 15px 15px 0 15px;
        margin: 10px 0;
        max-width: 80%;
        float: right;
        clear: both;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .assistant-msg {
        background-color: #2D2D2D;
        color: #E0E0E0;
        padding: 15px;
        border-radius: 15px 15px 15px 0;
        margin: 10px 0;
        max-width: 80%;
        float: left;
        clear: both;
        border: 1px solid #444;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(90deg, #bb86fc, #03dac6);
        color: black !important;
        font-weight: bold;
        border: none;
        border-radius: 8px;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(187, 134, 252, 0.4);
    }
</style>
""", unsafe_allow_html=True)

def initialize_app():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "db_initialized" not in st.session_state:
        init_db()
        st.session_state.db_initialized = True

initialize_app()

st.markdown('<div class="premium-title">Foundry Local RAG Assistant</div>', unsafe_allow_html=True)
st.markdown("💬 **Offline, private, and secure document Q&A powered by Microsoft Foundry Local.**")

# Sidebar for document management
with st.sidebar:
    st.header("📄 Knowledge Base")
    st.write("Upload PDF or TXT files to build your local knowledge base.")
    
    uploaded_files = st.file_uploader("Upload Documents", type=["pdf", "txt"], accept_multiple_files=True)
    
    if st.button("Ingest Documents 🚀"):
        if uploaded_files:
            with st.spinner("Processing documents and generating embeddings locally..."):
                clear_db()  # For simplicity, we clear and re-ingest in this demo
                total_chunks = 0
                for file in uploaded_files:
                    file_ext = file.name.split('.')[-1].lower()
                    chunks = ingest_document(file.name, BytesIO(file.read()), file_ext)
                    total_chunks += chunks
                st.success(f"✅ Successfully ingested {len(uploaded_files)} files into {total_chunks} chunks!")
        else:
            st.warning("Please upload some files first.")
            
    st.divider()
    st.info("💡 **How it works:**\n1. Documents are chunked.\n2. Local embeddings are generated.\n3. Vector search retrieves context.\n4. Local LLM answers using context.")

# Main Chat Interface
st.markdown("### Chat")

# Display chat history
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="user-msg">🧑‍💻 <b>You:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="assistant-msg">🤖 <b>Assistant:</b><br>{msg["content"]}</div>', unsafe_allow_html=True)

# Chat input
if query := st.chat_input("Ask a question about your documents..."):
    # Add user query to state
    st.session_state.messages.append({"role": "user", "content": query})
    st.markdown(f'<div class="user-msg">🧑‍💻 <b>You:</b><br>{query}</div>', unsafe_allow_html=True)
    
    # Generate and display assistant response
    with st.spinner("🧠 Thinking locally..."):
        answer = answer_query(query)
        
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.markdown(f'<div class="assistant-msg">🤖 <b>Assistant:</b><br>{answer}</div>', unsafe_allow_html=True)
    
    # Force a rerun to clean up layout float issues or just let it flow natively
    st.rerun()
