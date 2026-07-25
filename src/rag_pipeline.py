from .database import retrieve_top_k
from .ingestion import get_embedding_client, mgr
import foundry_local_sdk

def get_chat_client():
    models = mgr.catalog.list_models()
    
    # En iyi (en hızlı ve makul zekada) modelleri arıyoruz
    target_models = ['Phi-3.5-mini-instruct', 'qwen2.5-7b-instruct', 'qwen2.5-1.5b-instruct', 'qwen2.5-0.5b-instruct']
    selected_model = None
    
    for target in target_models:
        for m in models:
            if target.lower() in m.id.lower():
                selected_model = m
                break
        if selected_model:
            break
            
    if not selected_model:
        selected_model = mgr.catalog.get_model("qwen2.5-0.5b") # fallback
        
    if not selected_model:
        raise ValueError("Hiçbir uygun model bulunamadı!")
        
    if not selected_model.is_loaded:
        if not selected_model.is_cached:
            selected_model.download()
        selected_model.load()
    return selected_model.get_chat_client()

def answer_query(query: str, k: int = 2) -> str:
    """Answers a user query using the RAG pipeline."""
    try:
        # 1. Embed the user query directly
        embedding_client = get_embedding_client()
        response = embedding_client.generate_embedding(query)
        query_embedding = response.data[0].embedding
    except Exception as e:
        return f"Error embedding query: {e}"
        
    # 2. Retrieve relevant chunks
    top_chunks = retrieve_top_k(query_embedding, k=k)
    
    if not top_chunks:
        return "I don't have enough information in my knowledge base to answer that."
        
    # 3. Prepare the prompt
    context_text = "\n\n".join([
        f"KAYNAK BELGE: {chunk['doc_name']}\nMETİN: {chunk['content']}" 
        for chunk in top_chunks
    ])
    
    system_prompt = (
        "Sen bir yapay zeka asistanısın. Soruları KESİNLİKLE SADECE sana verilen metinlere göre cevapla.\n"
        "Kurallar:\n"
        "1. Eğer metinde sorunun cevabı net olarak YOKSA, kesinlikle uydurma ve yorum yapma. Sadece tek kelime olarak 'Bilmiyorum.' yaz.\n"
        "2. Cevap metinde varsa; kısa, anlaşılır ve düzgün bir Türkçe ile cevap ver.\n"
        "3. Cevabın en sonuna mutlaka kullandığın KAYNAK BELGE'nin adını ekle. Örnek: (Kaynak: ornek_belge.pdf)"
    )
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Aşağıdaki metinleri okuyarak soruyu cevapla.\n\nMETİNLER:\n{context_text}\n\nSORU: {query}"}
    ]
    
    # 4. Generate the response
    try:
        chat_client = get_chat_client()
        chat_response = chat_client.complete_chat(messages=messages)
        answer = chat_response.choices[0].message.content
        
        # Force source citation if model forgets (common with very small models)
        if "Kaynak:" not in answer:
            sources = list(set([chunk['doc_name'] for chunk in top_chunks]))
            answer += f"\n\n*(Kaynak: {', '.join(sources)})*"
            
        return answer
    except Exception as e:
        return f"Error generating answer: {e}"
