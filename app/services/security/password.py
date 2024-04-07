import bcrypt

ENCODING = "utf-8"


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(ENCODING), bcrypt.gensalt()).decode(ENCODING)


def check_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(ENCODING), hashed_password.encode(ENCODING))
