from fastapi import APIRouter



#For db session 
from app.core.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession



query_router=APIRouter()