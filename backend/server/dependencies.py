from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from server.models.user import User
from server.services.auth import decode_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    email = decode_access_token(token)
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = await User.find_one(User.email == email)
    if not user:
        raise HTTPException(status_code=401, detail="User not found. Invalid authentication credentials", headers={"WWW-Authenticate": "Bearer"})
    return User
