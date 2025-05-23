import uvicorn
from fastapi import FastAPI
from server.database import init_db
from contextlib import asynccontextmanager
from server.routes import event_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(event_router)

@app.get("/")
async def root():
    return {"message:": "Welcome to the PupCam backend server"}
