import os
from dotenv import load_dotenv
from pathlib import Path
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from server.models.device import Device
from server.models.user import User
from server.models.event import Event

# from server.models.camera import Camera

env_path = Path(__file__).resolve().parents[1].parents[0].parents[0] / "PupCam/.env"

load_dotenv(dotenv_path=env_path)
DB_NAME = os.getenv("DB_NAME")
MONGO_URI = os.getenv("MONGO_URI")

if not MONGO_URI:
    raise ValueError("MONGO_URI is not set in env")

if not DB_NAME:
    raise ValueError("DB_NAME is not set in env")


async def init_db():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]

    # add the rest of the models here
    try:
        await init_beanie(database=db, document_models=[Device, User, Event])

    except Exception as e:
        print("Beanie init failed:        ", e)
        raise
