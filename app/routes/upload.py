from fastapi import APIRouter, UploadFile, File, Depends, HTTPException

#For db session 
from app.core.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession

#Services
from app.services.pdf_reader import process_and_saving_uploaded_file


upload_router=APIRouter()


@upload_router.post("/")
async def upload_file(file: UploadFile = File(...),session: AsyncSession = Depends(get_session),):
    
    # Checking extension
    if not file.filename.lower().endswith((".pdf", ".txt", ".md")):
        raise HTTPException(status_code=400, detail="Formato file non supportato.")
    
    #Extract,reading,chunking and saving data on *POSTGRES*
    document_id = await process_and_saving_uploaded_file(file, session)

    

    
    return {"message": "File caricato con successo", "document_id": document_id}