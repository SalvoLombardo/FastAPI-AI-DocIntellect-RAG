from sqlalchemy import Column,Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
import uuid

Base=declarative_base()

def gen_uuid():
    return str(uuid.uuid4())

class Document(Base):
    __tablename__= 'documents'
    id= Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid())
    filename= Column(String, nullable=False)
    uploaded_at= Column(DateTime,default=datetime.utcnow)
    num_chunks= Column(Integer, default=0)
    raw_text= Column(Text)

    chunks= relationship("DocumentChunks", back_populates="document", cascade="all, delete-orphan")



class DocumentChunks(Base):
    pass
