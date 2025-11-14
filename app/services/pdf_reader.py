from sqlalchemy.ext.asyncio import AsyncSession
from app.models.document import Document,DocumentChunk
from datetime import datetime, timezone
from fastapi import UploadFile, HTTPException
from uuid import uuid4

import os

import pdfplumber
from io import BytesIO

async def process_uploaded_file(file : UploadFile, session:AsyncSession) -> str:
    try:
        content= await file.read()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Error during reading : {str(e)}')
    

    # Let's start by getting the extensio of the file 
    # If it's a PDF we will use pdf
    get_file_extension= os.path.splitext(file.filename)[1].lower()

    if get_file_extension=='.pdf':
        text= _extract_text_from_pdf(content)
    elif get_file_extension in [".txt",".md"]:
        text= _extract_text_from_txt(content)
    else:
        raise HTTPException(status_code=400, detail="Formato file non supportato.")
    
    #Create the dcuemnt object
    document=Document(
        id=str(uuid4()),
        filename=file.filename,
        created_at= datetime.now(timezone.utc)
    )
    session.add(document)


    #Chunks the text
    chunks= _split_text_into_chunks(text,chunks_size=500)

    #Creating with enumerate a documentchunk field
    for i, chunk_text in enumerate(chunks):
        chunk=DocumentChunk(
            id= str(uuid4()),
            document_id=document.id,
            chunck_index=i,
            text=chunk_text

        )
    session.add(chunk)

    try:
        await session.commit()
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f'Error during savng data on db: {str(e)}')

    return document.id



def _extract_text_from_pdf(content:bytes) ->str:

    text=''
    try:
        with pdfplumber.open(BytesIO(content)) as pdf:
            for page in pdf.pages:
                page_text=page.extract_text or ''#if is an empty page
                text += page_text + "\n"
    except Exception as e:
        raise HTTPException(status_code=500, detail='Someting goes wrong with reading session {str(e)}')
        
    if not text.strip():#?????????
        raise HTTPException (status_code=400, detail="Not readble text here")
    
    return text

def _extract_text_from_txt(content:bytes) ->str:

    try:
        text_decode= content.decode('utf-8')
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Errors in decoding session {str(e)}')
    
    return text_decode

def _split_text_into_chunks(text: str, chunk_size: int = 500) -> list[str]:
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
    return chunks