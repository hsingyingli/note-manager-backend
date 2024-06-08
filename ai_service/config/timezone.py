from functools import lru_cache

from pytz import timezone

from config.setting import Settings

settings = Settings()


@lru_cache
def get_timezone():
    return timezone(settings.timezone)
