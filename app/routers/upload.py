import os
from uuid import uuid4
from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from app.utils.deps import require_role
from app.models.user import Role
from app.utils.file_parser import extract_text_from_file


UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter(prefix="/upload", tags=["upload"])

@router.post("/document")
async def upload_document(
    file: UploadFile = File(...),
    user=Depends(require_role(Role.client))
):
    allowed_types = ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                     "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "image/png", "image/jpeg"]
    
    if file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    
    extension = file.filename.split(".")[-1]
    filename = f"{uuid4()}.{extension}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
        
    extracted_text = extract_text_from_file(file_path, file.content_type)

    return { "filename": filename,
        "content_type": file.content_type,
        "text": extracted_text[:500], 
        "message": "File uploaded and parsed successfully"}
