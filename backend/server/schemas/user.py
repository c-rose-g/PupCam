# schemas/user.py

# Register, login, profile
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
  email: EmailStr
  name: str
  password: str

class UserLogin(BaseModel):
  email: EmailStr
  password: str

class UserResponse(BaseModel):
  id: str
  email: EmailStr
  name: str

  class Config:
    from_attributes = True
class UserUpdate(BaseModel):
  email: EmailStr
  name: str
  password:str

class UserPatch(BaseModel):
  email: Optional[EmailStr] = None
  name: Optional[str] = None
  password: Optional[str] = None
