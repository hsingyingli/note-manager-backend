import uuid
from datetime import datetime, timedelta
from typing import Tuple

import jwt
from pydantic import BaseModel

from app.utils.monadic import monadic
from config.setting import Settings
from config.timezone import get_timezone

settings = Settings()

timezone = get_timezone()


class Payload(BaseModel):
    id: str
    iat: datetime
    exp: datetime
    email: str


def create_payload(email: str, duration_in_seconds: int) -> Payload:
    issued_at = datetime.now(timezone)
    payload = {
        "id": str(uuid.uuid4()),
        "iat": issued_at,
        "exp": issued_at + timedelta(seconds=duration_in_seconds),
        "email": email,
    }
    return Payload(**payload)


def create_token(email: str, duration_in_seconds: int) -> Tuple[str, Payload]:
    payload = create_payload(email, duration_in_seconds)
    return (
        jwt.encode(payload.model_dump(), settings.symmetric_key, algorithm="HS256"),
        payload,
    )


@monadic
def verify_token(encoded) -> Payload:
    return Payload(**jwt.decode(encoded, settings.symmetric_key, algorithms="HS256"))
