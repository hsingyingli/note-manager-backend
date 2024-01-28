from pytz import timezone

from config.setting import Settings

settings = Settings()


def get_timezone():
    return timezone(settings.timezone)
