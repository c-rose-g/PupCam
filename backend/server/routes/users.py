from fastapi import APIRouter, HTTPException
from typing import List, Optional, Dict
from beanie import PydanticObjectId
from servers.models.user import User

router = APIRouter(prefix="/users", tags=["Users"])

