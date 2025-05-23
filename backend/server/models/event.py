from datetime import datetime, timezone

from beanie import Document, before_event, Insert
from pydantic import BaseModel, Field
from typing import Optional

class TimeStamp(Document):
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))


class Event(TimeStamp):
    """
    Event model for storing events in the database.
    """
    event_type: str
    image_url: str
    video_url: str

    class Settings:
        name = "event_collection"

    class Config:
        schema_extra = {
            "example": {
                "event_type": "motion",
                "image_url": "https://example.com/image.jpg",
                "video_url": "https://example.com/video.mp4",
                "created_at": datetime.now()
            }
        }
