import chromadb
from chromadb.api.types import Documents,Embeddings,Metadatas, IDs


client = chromadb.Client()
collection= client.get_or_create_collection(name='document_chunks')

async def add_chunk_to_chroma(chunk_id: str, text: str, embedding: list[float], metadata: dict):
    collection.add(
        ids=[chunk_id],
        documents=[text],
        embeddings=[embedding],
        metadata=[metadata]
    )


async def query_chroma(embedding: list[float], top_k: int =5):
    results=collection.query(query_embeddings=[embedding], n_results= top_k)

    return results
    
