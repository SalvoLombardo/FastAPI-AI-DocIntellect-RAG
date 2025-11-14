from sqlalchemy.ext.asyncio import AsyncSession
from app.models.document import Document, DocumentChunk
from datetime import datetime, timezone
from fastapi import UploadFile, HTTPException
from uuid import uuid4
import os
import pdfplumber
from io import BytesIO

from app.utils.chunking import split_text_into_chunks


async def process_and_saving_uploaded_file(file: UploadFile, session: AsyncSession) -> str:
    # Reading file
    try:
        content= await file.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during file reading: {str(e)}")

    #Getting the extension of the file (splitex return a tuple, nameoffile and extension) that's why [1]
    ext = os.path.splitext(file.filename)[1].lower()

    
    # Deciding with service func to use
    if ext ==".pdf":
        text, metadata=_extract_text_from_pdf(content)
    elif ext in [".txt", ".md"]:
        text =_extract_text_from_txt(content)
    else:
        raise HTTPException(status_code=400, detail="Formato file non supportato.")

    # creating the record docuemnt
    document = Document(
        id=str(uuid4()),
        filename=file.filename,
        content_type=file.content_type,
        created_at=datetime.now(timezone.utc),
        metadata=metadata
    )
    session.add(document)

    # Chuncking the text and getting the len oof the chunks for later
    chunks = split_text_into_chunks(text, chunk_size=500)
    document.num_chunks = len(chunks)

    #Saving chunks with enumerate, using i to have the right sequency of the chunks
    for i, chunk_text in enumerate(chunks):
        chunk = DocumentChunk(
            id=str(uuid4()),
            document_id=document.id,
            chunk_index=i,
            text=chunk_text
        )
        session.add(chunk)

    #Committing or rollback
    try:
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Error during DB write: {str(e)}")

    return document.id


def _extract_text_from_pdf(content: bytes) -> tuple[str, dict]:
    text = ""
    metadata = {}

    try:
        with pdfplumber.open(BytesIO(content)) as pdf:
            # Getting Metadata if they exists or empty{}
            metadata = pdf.metadata or {}

            
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                text += page_text + "\n"

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading PDF: {str(e)}")

    if not text.strip(): #If after text.strip() that removes every spaces, there's nothing remains it's an non readable file
        raise HTTPException(status_code=400, detail="Il PDF non contiene testo leggibile.")

    return text, metadata


def _extract_text_from_txt(content: bytes) -> str:
    try:
        return content.decode("utf-8")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error decoding TXT: {str(e)}")
