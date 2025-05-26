from datetime import datetime, timezone
from typing import Optional
from beanie import Document
from pydantic import Field, ConfigDict, field_validator, EmailStr
from bson import ObjectId
import re

class User(Document):
    """
    User model
    # serial_number: str (for later)
    # registered_at: datetime = Field(default=datetime.now(timezone.utc)) make sure this doesn't change
    # limit number of failed login attempts on a single account to prevent brute-force attacks
    # allow users to past passwords from a password manager
    # salt and hash password (do I do this here?)
    # verify passwords against known compromised or weak password lists (how do I do that?)
    # enforce MFA or authentication (for later)
    """
    email: EmailStr
    name: str
    hashed_password: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        if "@" not in value:
            raise ValueError("Email must contain '@'.")
        if not value.empty():
            raise ValueError("Email field cannot be empty.")
        return value

    class Settings:
        name = "user_collection"

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},
        json_schema_extra={
            "example": {
                "email": "test@example.com",
                "hashed_password": "StrongP@ssword123456789",
                "created_at": datetime.now()
            }
        }
    )

class UserInDB(User):
    hashed_password: str
