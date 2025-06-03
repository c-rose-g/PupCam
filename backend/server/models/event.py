# models/event.py
from datetime import datetime, timezone
from typing import Optional, Literal
from beanie import Document
from pydantic import Field, ConfigDict, field_validator, HttpUrl
from bson import ObjectId
from server.models.user import User
class Event(Document):
    """
    Event model for storing motion detection events in the database.

    I'll use Literal type for event_type for now, but may change to enum later if I have more different values to represent.
    Literal type has a built-in validator
    Create an compound index (id, user_id, created_at)
    create partial index (id, created_at)
    """
    event_type: Literal["motion", "sound"]
    image_url: HttpUrl
    video_url: str
    user_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    class Settings:
        name = "event_collection"

    # class Config:
    #     from_attributes = True

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "event_type": "motion",
                "image_url": "https://example.com/image.jpg",
                "video_url": "https://example.com/video.mp4",
                "user_id" "test_dev_id"
                "timestamp": datetime.now()
            }
        }
    )
