from fastapi import APIRouter, HTTPException
from typing import List, Optional, Dict
from beanie import PydanticObjectId
from server.models.user import User

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/")
async def get_all_users():
  # return {"message":"you've reached the user endpoint."}
  return await User.find_all().to_list()
