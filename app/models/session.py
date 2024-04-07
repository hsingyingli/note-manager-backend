from datetime import datetime

from pydantic import UUID4, BaseModel


class Session(BaseModel):
    id: UUID4
    user_id: int = None
    created_at: datetime = None
    updated_at: datetime = None
    expired_at: datetime = None
    refresh_token: str = None
