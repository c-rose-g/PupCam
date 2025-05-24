from fastapi import APIRouter, HTTPException
from typing import List, Optional, Dict
from beanie import PydanticObjectId
from server.models.user import User

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/")
async def get_all_users():
  return await User.find_all().to_list()

@router.post("/")
async def create_user(user: User):
  await User.create()
  return user

@router.get("/{user_id}")
async def get_user_by_id():
  user = await User.find_one(user_id = str)
  return user
