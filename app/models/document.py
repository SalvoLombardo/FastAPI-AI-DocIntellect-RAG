import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import registry, relationship
from datetime import datetime, timezone
import uuid

mapper_registry = registry()
Base = mapper_registry.generate_base()

def gen_uuid():
    return str(uuid.uuid4())

class Document(Base):
    __tablename__ = "documents"

    id = sa.Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    filename = sa.Column(sa.String(255), nullable=False)
    content_type = sa.Column(sa.String(100))
    num_chunks = sa.Column(sa.Integer, default=0)
    metadata_info = sa.Column(JSONB, nullable=True) #Using JSONB Postgres special data for JSON style
    created_at = sa.Column(sa.DateTime(timezone=True), default=datetime.now(timezone.utc))

    chunks = relationship("DocumentChunk", back_populates="document", cascade="all, delete-orphan")

class DocumentChunk(Base):
    __tablename__ = "document_chunks"

    id = sa.Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid)
    document_id = sa.Column(UUID(as_uuid=False), sa.ForeignKey("documents.id", ondelete="CASCADE"), nullable=False, index=True)
    chunk_index = sa.Column(sa.Integer, nullable=False)
    text = sa.Column(sa.Text, nullable=False)
    chroma_id = sa.Column(sa.String(255), nullable=True, index=True)
    token_count = sa.Column(sa.Integer, nullable=True)
    created_at = sa.Column(sa.DateTime(timezone=True), default=datetime.now(timezone.utc))

    document = relationship("Document", back_populates="chunks")