from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.setting import Settings

settings = Settings()


def get_database_dsn() -> str:
    return f"{settings.db_driver}://{settings.db_user}:{settings.db_password}@{settings.db_host}:{settings.db_port}/{settings.db_name}"


def get_engine():
    engine = create_engine(get_database_dsn(), connect_args={})
    return engine


def get_db_session():
    db = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())()
    try:
        yield db
    finally:
        db.close()
