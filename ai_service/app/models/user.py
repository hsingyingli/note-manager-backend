from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    id: int = Field(exclude=True)
    username: str = Field(pattern=r"^[0-9a-zA-Z]{6,18}$", default=None)
    email: EmailStr = None
    password: str = Field(max_length=256, default=None, exclude=True)
    created_at: datetime = None
    updated_at: datetime = None
