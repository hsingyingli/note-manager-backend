import uuid
from datetime import datetime, timedelta

from pydantic import BaseModel

from app.utils.date import get_timezone

timezone = get_timezone()


class Payload(BaseModel):
    id: uuid.UUID
    iat: datetime
    exp: datetime
    user_id: int


def create_payload(user_id: int, duration_in_seconds: int) -> Payload:
    issued_at = datetime.now(timezone)
    payload = {
        "id": uuid.uuid4(),
        "iat": issued_at,
        "exp": issued_at + timedelta(seconds=duration_in_seconds),
        "user_id": user_id,
    }
    return Payload(**payload)
