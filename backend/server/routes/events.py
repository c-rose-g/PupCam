from fastapi import APIRouter, HTTPException
from typing import List, Optional, Dict
from beanie import PydanticObjectId
from server.models.event import Event

router = APIRouter(prefix="/events", tags=["Events"])

@router.get("/")
async def get_all_events():
  return await Event.find_all().to_list()

@router.get("/{event_id}")
async def get_event_by_id(event_id: str):
  try:
    obj_id = PydanticObjectId(event_id)
  except Exception:
    raise HTTPException(status_code=422, detail="Invalid ObjectId format")

  event = await Event.get(obj_id)
  return event
