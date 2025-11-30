from app.core.embeddings import get_embedding
from app.services.chroma_service import query_chroma

from openai import OpenAI

client= OpenAI()

async def rag_query(user_query: str, top_k: int =1):

    #Embedding the query
    query_embedding= get_embedding(user_query)

    #Quering on Chroma
    chroma_results= await query_chroma(query_embedding, top_k=top_k)

    if not chroma_results['documents']:
        return "I didn't find inherent documents"
    
    # Extracting results
    chunks = chroma_results['documents']

    # estrai i testi dai documenti
    chunks_nested = chroma_results['documents']  # lista di liste
    chunks = [chunk for doc in chunks_nested for chunk in doc]  # flatten

    
    context = "\n\n--\n\n".join(chunks)

    prompt= f"""
You're an RAG assistant, Reply to the USER_QUERY with only information inside CONTEXT.
If the information is not in the CONTEXT, reply that is not available

CONTEXT:
{context}

USER_QUERY:
{user_query}

ANSWER: 
"""
    
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    answer = response.choices[0].message.content
    return answer


