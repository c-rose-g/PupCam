import uvicorn
from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer
from server.database import init_db
from contextlib import asynccontextmanager
from server.routes import device_router
from server.routes import user_router
from server.routes import event_router
from server.routes import auth_router

from typing import Annotated


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(device_router)
app.include_router(event_router)

@app.get("/")
async def root(token: Annotated[str, Depends(oauth2_scheme)]):

    return {"message:": "Welcome to the PupCam backend server. Please use the http://127.0.0.1:8000/docs endpoint to see the API documentation.",
            "token": token}
