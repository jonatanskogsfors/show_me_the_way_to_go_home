import datetime
from typing import Union

time_or_date = Union[datetime.time, datetime.datetime]


def next_five_minutes(timepoint: time_or_date) -> time_or_date:
    past_five = timepoint.minute % 5
    if past_five != 0:
        rounded_minute = timepoint.minute + (5 - past_five)
    else:
        rounded_minute = timepoint.minute
    rounded_datetime = timepoint.replace(minute=rounded_minute)
    return rounded_datetime
