import os
from dotenv import load_dotenv
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from server.models.event import Event
# from server.models.user import User
# from server.models.camera import Camera

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DV_NAME")

async def init_db():
  client = AsyncIOMotorClient(MONGO_URI)
  db = client[DB_NAME]

  await init_beanie(database=db, document_models=[Event])
