# schemas/event.py
# CreateEventRequest, EventResponse
from typing import Literal
from pydantic import BaseModel, HttpUrl
from datetime import datetime, timezone
class EventCreate(BaseModel):
  event_type: Literal["motion","sound"]
  image_url: HttpUrl
  video_url: str
  timestamp: datetime

class EventResponse(BaseModel):
  id: str
  event_type: Literal["motion","sound"]
  image_url: HttpUrl
  video_url: str

  class Config:
    from_attributes = True
