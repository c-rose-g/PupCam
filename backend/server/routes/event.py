from fastapi import APIRouter, HTTPException
from typing import List
from server.models.event import Event

router = APIRouter("/events", tags=["Events"])

@router.get("/", response_model=List[Event])
async def get_all_events():
  return await Event.find_all().to_list()
