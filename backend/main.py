# add mongoDB + Beanie setup
from fastapi import FastAPI
from beanie import init_beanie
# from models.event import Event
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()
MONGO_URL = os.getenv("MONGO_URL")
DB_NAME = os.getenv("DB_NAME", "pupcam")
app = FastAPI()

@app.get("/")
async def root():
  return {"message": "Hello World"}
