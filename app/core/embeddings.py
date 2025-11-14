# app/core/embeddings.py
from openai import OpenAI

client = OpenAI()

async def get_embedding(text: str) -> list[float]:
    response = await client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding