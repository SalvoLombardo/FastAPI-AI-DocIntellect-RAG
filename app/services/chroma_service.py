import chromadb
from chromadb.config import Settings
from chromadb.api.types import Documents, Embeddings, Metadatas, IDs

# Configura ChromaDB con persistenza
client = chromadb.Client(Settings(
    chroma_db_impl="duckdb+parquet",   
    persist_directory="./chroma_db"    # cartella dove salvare i dati
))

# Crea o prendi la collection
collection_name = "document_chunks"
if collection_name in [c.name for c in client.list_collections()]:
    collection = client.get_collection(collection_name)
else:
    collection = client.create_collection(collection_name)




async def query_chroma(embedding: list[float], top_k: int = 1):
    results = collection.query(
        query_embeddings=[embedding],
        n_results=top_k
    )
    return results