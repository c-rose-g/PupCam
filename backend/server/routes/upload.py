from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
import motor.motor_asyncio
import gridfs
from typing import List, Optional, Dict
from beanie import PydanticObjectId

router = APIRouter(prefix="/upload", tags=["Upload"])
