from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class User(BaseModel):
    id: int
    username: str = Field(pattern=r"^[0-9a-zA-Z]{6,18}$", default=None)
    email: EmailStr = None
    password: str = Field(max_length=256, default=None)
    created_at: datetime = None
    updated_at: datetime = None
