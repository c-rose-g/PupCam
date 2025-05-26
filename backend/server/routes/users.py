from fastapi import APIRouter, HTTPException, Depends
from server.models.user import User
from server.dependencies import get_current_user
from server.models.user import User
from server.schemas.user import UserResponse, UserUpdate, UserPatch
from server.services.auth import hash_password

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/")
async def get_all_users():
    return await User.find_all().to_list()


@router.get("/me", response_model=UserResponse)
async def read_user_me(current_user: User = Depends(get_current_user)):
    return UserResponse(id=str(current_user.id), email=current_user.email, name=current_user.name)


@router.get("/{user_id}", response_model=UserResponse)
async def read_user_by_id(user_id: str):
    user = await User.find_one(user_id)
    return user

@router.patch("/{user_id}", response_model=UserResponse)
async def update_user_partial(user_id: str, updated_data: UserPatch, current_user: User = Depends(get_current_user)):

    if str(current_user) != user_id:
        raise HTTPException(
            status_code=403, description="Not authorized to update this user.")

    user = await User.get(user_id)
    if not user:
        raise HTTPException(status_code=404, description="User not found.")

    if updated_data.name is not None:
        user.name = updated_data.name
    if updated_data.email is not None:
        user.email = updated_data.email
    if updated_data.password is not None:
        user.hashed_password = hash_password(updated_data.password)

    await user.save()
    return user


@router.put("/{user_id}", response_model=UserResponse)
async def update_user_by_id(user_id: str, updated_data: UserUpdate):
    user = await User.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.name = updated_data.name
    user.email = updated_data.email
    if updated_data.password:

        user.hashed_password = hash_password(updated_data.password)

    await user.save()
    return user

@router.delete("/{user_id}", status_code=204)
async def delete_user_by_id(user_id: str):
    user = await User.get(user_id)
    if not user:
        raise HTTPException(status_code=404, description="User not found.")
    
    await user.delete()
    return None
