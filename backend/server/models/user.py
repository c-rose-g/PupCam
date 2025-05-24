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

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        if not value.include("@"):
            raise ValueError("Email must contain '@'.")
        if not value.empty():
            raise ValueError("Email field cannot be empty.")
        return value

    @field_validator("hashed_password")
    @classmethod
    def validate_password(cls, value):

        if len(value) < 16:
            raise ValueError(
                "Password must be at least 16 characters long.")

        if not re.search(r"[a-z]", value):
            raise ValueError(
                "Password must contain at least one lowercase character.")
        if not re.search(r"[A-Z]", value):
            raise ValueError(
                "Password must contain at least one uppercase character.")
        if not re.search(r"[0-9]", value):
            raise ValueError("Password must contain at least one digit.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError(
                "Password must contain at least one special character:!@#$%^&*(),.?\":{}|<>")
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
