import time as _time

from datetime import date as dtdate
from datetime import datetime, time, timedelta


def datetime_to_timestamp(date):
    if isinstance(date, datetime):
        pass
    elif isinstance(date, dtdate):
        date = datetime.combine(date, time.min)

    return int(
        (date - datetime(1970, 1, 1) - timedelta(hours=8)).total_seconds() * 1000
    )


def timestamp_to_format_time(tp):
    return datetime.fromtimestamp(float(tp) / 1000).strftime("%Y-%m-%d %H:%M:%S")


def expire_date(day=7):
    """
    默认7天后的时间戳
    """
    return int(_time.time() * 1000) + day * 24 * 60 * 60 * 1000


def date_to_datetime(date):
    return datetime.combine(date, time.min)
