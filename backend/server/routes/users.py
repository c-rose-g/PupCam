from fastapi import APIRouter, HTTPException, Depends, FastAPI
from typing import List, Optional, Dict, Annotated
from beanie import PydanticObjectId
from fastapi.security import OAuth2PasswordBearer
from server.models.user import User

router = APIRouter(prefix="/users", tags=["Users"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def fake_decode_token(token):
    return User(
        username=token + "fakedecoded", email="jane@example.com", full_name="Jane Doe"
    )


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    return user


@router.get("/")
async def get_all_users():
    return await User.find_all().to_list()


@router.get("/me")
async def read_user_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user


@router.get("/{user_id}")
async def read_user_by_id():
    user = await User.find_one(user_id=str)
    return user

@router.put("/{user_id}")
async def update_user_by_id():
    user = await User.find_one(user_id=str)

    if not user:
        raise ValueError("user does not exist")

    User.update()
