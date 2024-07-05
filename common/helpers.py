import pytz
from datetime import datetime

from core.settings import TIME_ZONE


def datetime_now() -> datetime:
    """
    function that returns the current date

    :return: datetime: Current date
    """
    return datetime.now(tz=pytz.timezone(TIME_ZONE))
