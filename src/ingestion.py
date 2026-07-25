import os
from io import BytesIO
from typing import List, Union
import pdfplumber
import foundry_local_sdk
from .database import insert_chunk, clear_db, init_db

# Initialize Foundry Local Manager once
if foundry_local_sdk.FoundryLocalManager.instance is None:
    conf = foundry_local_sdk.Configuration(app_name="RAGAssistant")
    foundry_local_sdk.FoundryLocalManager.initialize(conf)
mgr = foundry_local_sdk.FoundryLocalManager.instance

def get_embedding_client():
    model = mgr.catalog.get_model("qwen3-embedding-0.6b")
    if not model:
        raise ValueError("qwen3-embedding-0.6b model not found in catalog!")
    if not model.is_loaded:
        if not model.is_cached:
            model.download()
        model.load()
    return model.get_embedding_client()

def extract_text(file_obj: BytesIO, file_type: str) -> str:
    text = ""
    if file_type == "pdf":
        with pdfplumber.open(file_obj) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
    elif file_type == "txt":
        text = file_obj.read().decode("utf-8")
    return text

def chunk_text(text: str, chunk_size: int = 800, overlap: int = 150) -> List[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += (chunk_size - overlap)
    return chunks

def ingest_document(file_name: str, file_obj: BytesIO, file_type: str):
    """Extracts text from a file, chunks it, generates embeddings, and saves to DB."""
    text = extract_text(file_obj, file_type)
    if not text.strip():
        return 0
    
    chunks = chunk_text(text)
    
    try:
        embedding_client = get_embedding_client()
    except Exception as e:
        print(f"Error loading embedding model: {e}")
        return 0
    
    chunk_count = 0
    for i, chunk in enumerate(chunks):
        if not chunk.strip():
            continue
        try:
            # Generate embedding
            response = embedding_client.generate_embedding(chunk)
            embedding_vector = response.data[0].embedding
            
            # Save to SQLite
            insert_chunk(file_name, i, chunk, embedding_vector)
            chunk_count += 1
        except Exception as e:
            print(f"Error embedding chunk {i}: {e}")
            
    return chunk_count

