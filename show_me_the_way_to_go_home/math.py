def next_five_minutes(datetime):
    past_five = datetime.minute % 5
    if past_five != 0:
        rounded_minute = datetime.minute + (5 - past_five)
    else:
        rounded_minute = datetime.minute
    rounded_datetime = datetime.replace(minute=rounded_minute)
    return rounded_datetime
