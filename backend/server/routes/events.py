from fastapi import APIRouter, HTTPException
from typing import List, Optional, Dict
from beanie import PydanticObjectId
from server.models.event import Event

router = APIRouter(prefix="/events", tags=["Events"])

@router.post("/{event_id}")
async def create_event(event: Event):
  await event.create()
  return event

@router.get("/")
async def get_all_events():
  return await Event.find_all().to_list()

@router.get("/{event_id}")
async def get_event_by_id(event_id: str):

  event = await Event.get(event_id)
  return event
