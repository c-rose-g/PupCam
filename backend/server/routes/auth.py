# /register, /login
from fastapi import APIRouter, HTTPException, Depends
from server.schemas.user import UserCreate, UserLogin, UserResponse
from server.models.user import User
from server.services.auth import hash_password, verify_password, create_access_token
from beanie.exceptions import DocumentNotFound
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()


@router.post("/register", response_model=UserResponse)
async def register(user: UserCreate):
    existing = await User.find_one(User.email == user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = hash_password(user.password)
    new_user = User(email=user.email, name=user.name, hashed_password=hashed)
    await new_user.insert()
    return UserResponse(
        id=str(new_user.id),
        email=new_user.email,
        name=new_user.name
    )


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await User.find_one(User.email == form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials :(")
    token = create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}
