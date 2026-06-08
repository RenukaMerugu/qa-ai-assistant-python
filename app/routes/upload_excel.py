import os
from fastapi import APIRouter, UploadFile, File

UPLOAD_FOLDER = "uploads"
router = APIRouter()

@router.post("/upload-excel")
async def upload_excel(file: UploadFile = File(...)):

    filepath = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    with open(filepath, "wb") as f:
        f.write(await file.read())

    return {
        "message": "uploaded",
        "file": filepath
    }