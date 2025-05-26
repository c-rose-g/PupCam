# routes/events.py
from fastapi import APIRouter, HTTPException
from typing import List, Optional, Dict
from beanie import PydanticObjectId
from server.models.event import Event
from server.schemas.event import EventCreate, EventResponse
router = APIRouter(prefix="/events", tags=["Events"])


@router.post("/", response_model=EventResponse)
async def create_event(event_data: EventCreate):
    event = Event(**event_data.model_dump())
    await event.create()

    return EventResponse(
        id=str(event.id),
        event_type=event.event_type,
        image_url=event.image_url,
        video_url=event.video_url,
        user_id=event.user_id,
        timestamp=event.timestamp
    )


@router.get("/", response_model=List[EventResponse])
async def get_all_events():
    events = await Event.find_all().to_list()
    return [EventResponse(id=str(event.id), event_type=event.event_type, image_url=event.image_url, video_url=event.video_url, user_id=event.user_id, timestamp=event.timestamp)
            for event in events
            ]


@router.get("/{event_id}", response_model=EventResponse)
async def get_event_by_id(event_id: str):
    event = await Event.get(event_id)

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return EventResponse(
        id=str(event.id),
        event_type=event.event_type,
        image_url=event.image_url,
        video_url=event.video_url,
        user_id=event.user_id,
        timestamp=event.timestamp,
    )
