from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from server.database import fs

router = APIRouter(prefix="/upload", tags=["Upload"])

@router.post("/")
async def upload_video(file: UploadFile = File(...)):
    contents = await file.read()
    file_id = await fs.upload_from_stream(file.filename, contents)
    return JSONResponse({"video_url": str(file_id)})
