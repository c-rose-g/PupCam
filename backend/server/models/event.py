from datetime import datetime, timezone
from typing import Optional, Literal
from beanie import Document
from pydantic import Field, ConfigDict, field_validator
from bson import ObjectId
from server.models.user import User

class TimeStamp(Document):
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc))


class Event(TimeStamp, User):
    """
    Event model for storing motion detection events in the database.

    I'll use Literal type for event_type for now, but may change to enum later if I have more different values to represent.
    Literal type has a built-in validator
    Create an compound index (id, user_id, created_at)
    create partial index (id, created_at)
    """
    event_type: Literal["motion", "sound"]
    image_url: str
    video_url: str
    user_id: str

    @field_validator("image_url")
    @classmethod
    def validate_image_url(cls, value):
        if not value.startswith("https://"):
            raise ValueError("Image URL must start with 'https://'")
        return value

    @field_validator("video_url")
    @classmethod
    def validate_video_url(cls, value):
        if not value.startswith("https://"):
            raise ValueError("Video URL must start with 'https://'")
        return value

    class Settings:
        name = "event_collection"

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "event_type": "motion",
                "image_url": "https://example.com/image.jpg",
                "video_url": "https://example.com/video.mp4",
                "created_at": datetime.now()
            }
        }
    )
