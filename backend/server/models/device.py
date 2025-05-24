from datetime import time, datetime, timedelta, timezone
from typing import Optional, Literal, List, Dict
from beanie import Document, PydanticObjectId
from pydantic import Field, ConfigDict, field_validator
from bson import ObjectId
from server.models.user import User  # do I import indexes too?
from server.models.event import Event, TimeStamp


class Device(TimeStamp):  # do I add Events as well?
    """
    Device schema
    how do i get location? do i event need it for mvp?

    """
    device_name: str
    owner_id: str  # do I validate user, or create an index?
    events: List[Event]
    alert_enabled: bool  # make default false
    quiet_hour_start: Optional[time]  # start <= current_time
    quiet_hour_end: str  # end >= current_time
    schedule: Optional[Dict] = None
    bark_enabled: bool

    @field_validator("quiet_hour_start", "quiet_hour_end")
    @classmethod
    def validate_hour_start(cls, value: str):
        # convert (hh:mm) to time obj
        if value is not None:
            hour, minute = map(int, value.splt[":"])
            return time(hour, minute)
        return None

    class Settings:
        name = "device_collection"

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "device_name": "camera_0",
                "owner_id": "1",
                "events": "[event01, event02]",
                "alerts_enabled": "false",
                "quiet_hour_start": "start:current_time",
                "quiet_hour_end": "end:current_time",
                "schedule": {
                  "day_of_week": {
                    "$and": [{"start_hour": {"$lte": datetime.now().time()}},
                             {"end_hour": {"$gte": datetime.now().strftime("%A").lower()}}
                             ]
                    }
                },
                "bark_enabled": "false",
                "registered_at": datetime.now()
            }
        }
    )

# class Schedule(Document):
#   schedules = Optional[Dict]

#   class Settings:
#     name = "schedule_collection"
