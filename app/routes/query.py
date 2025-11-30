from fastapi import APIRouter



#For db session 
from app.core.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.rag_service import rag_query

from app.schemas.document import QueryRequest


query_router=APIRouter()



@query_router.post("/query")
async def ask_rag(body: QueryRequest):
    answer = await rag_query(body.query)
    return {"answer": answer}