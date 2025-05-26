# CreateEventRequest, EventResponse
from pydantic import BaseModel
from datetime import datetime

class EventCreate(BaseModel):
  type: str
  snapshot_url: str

class EventResponse(BaseModel):
  id: str
  type: str
  timestamp: datetime
  snapshot_url: str
