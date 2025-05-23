from datetime import datetime, timezone
from typing import Optional
from beanie import Document
from pydantic import Field, ConfigDict
from bson import ObjectId


class TimeStamp(Document):
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))


class Event(TimeStamp):
    """
    Event model for storing motion detection events in the database.
    """
    id: str = Field(default=None, alias="_id")
    event_type: str
    image_url: str
    video_url: str

    class Settings:
        name = "event_collection"

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        schema_extra = {
            "example": {
                "event_type": "motion",
                "image_url": "https://example.com/image.jpg",
                "video_url": "https://example.com/video.mp4",
                "created_at": datetime.now()
            }
        }
        )
