# db/session.py
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from dotenv import load_dotenv
import os
from app.models.document import Base  
from collections.abc import AsyncGenerator

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set up in .env")




engine = create_async_engine(
    DATABASE_URL,
    future=True # To use the synthax of SQLAlchemy 2.0
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession # to specify to use 
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try: 
            yield session
        finally:
            pass