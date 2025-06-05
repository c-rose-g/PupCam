from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
from fastapi.responses import JSONResponse
from server.database import fs
import os

router = APIRouter(prefix="/upload", tags=["Upload"])

@router.post("/")
async def upload_video(file: UploadFile = File(...)):
    try:
        if not file.filename:
            raise HTTPException(status_code=400, detail="No filename provided.")

        save_path = os.path.join("static", "videos", file.filename)

        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {"video_url": f"/static/videos/{file.filename}"}

    except Exception as e:
        print("UPLOAD ROUTE ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))
    # contents = await file.read()
    # video_url = await fs.upload_from_stream(file.filename, contents)
    # return JSONResponse({"video_url": str(video_url)})

# /play-latest
