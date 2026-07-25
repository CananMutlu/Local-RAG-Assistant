import sqlite3
import json
import math
from typing import List, Tuple, Dict, Any

DB_PATH = "rag_knowledge.db"

def init_db():
    """Initialize the SQLite database and create the documents table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            doc_name TEXT NOT NULL,
            chunk_index INTEGER NOT NULL,
            content TEXT NOT NULL,
            embedding TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def insert_chunk(doc_name: str, chunk_index: int, content: str, embedding: List[float]):
    """Insert a single document chunk and its embedding into the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    embedding_str = json.dumps(embedding)
    cursor.execute('''
        INSERT INTO documents (doc_name, chunk_index, content, embedding)
        VALUES (?, ?, ?, ?)
    ''', (doc_name, chunk_index, content, embedding_str))
    conn.commit()
    conn.close()

def clear_db():
    """Clear all records from the documents table."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM documents')
    conn.commit()
    conn.close()

def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    """Compute the cosine similarity between two vectors."""
    if not v1 or not v2 or len(v1) != len(v2):
        return 0.0
    dot_product = sum(a * b for a, b in zip(v1, v2))
    norm_v1 = math.sqrt(sum(a * a for a in v1))
    norm_v2 = math.sqrt(sum(b * b for b in v2))
    if norm_v1 == 0 or norm_v2 == 0:
        return 0.0
    return dot_product / (norm_v1 * norm_v2)

def retrieve_top_k(query_embedding: List[float], k: int = 3) -> List[Dict[str, Any]]:
    """Retrieve the top k most similar chunks to the query embedding."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT doc_name, chunk_index, content, embedding FROM documents')
    rows = cursor.fetchall()
    conn.close()
    
    results = []
    for row in rows:
        doc_name, chunk_index, content, embedding_str = row
        chunk_embedding = json.loads(embedding_str)
        similarity = cosine_similarity(query_embedding, chunk_embedding)
        results.append({
            'doc_name': doc_name,
            'chunk_index': chunk_index,
            'content': content,
            'similarity': similarity
        })
    
    # Sort by similarity descending and pick top k
    results.sort(key=lambda x: x['similarity'], reverse=True)
    return results[:k]
