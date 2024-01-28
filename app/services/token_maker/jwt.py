import jwt

from config.setting import Settings

from .payload import Payload, create_payload

settings = Settings()


def create_token(user_id: int, duration_in_second: int) -> str:
    payload = create_payload(user_id, duration_in_second)
    return jwt.encode(payload.model_dump(), settings.symmetric_key, algorithm="HS256")


def verify_token(encoded):
    return Payload(**jwt.decode(encoded, settings.symmetric_key, algorithms="HS256"))
