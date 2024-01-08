from datetime import datetime
from dateutil import tz


def time_ago(timestamp):
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()

    current_time = datetime.utcnow()
    time_difference = current_time - timestamp
    # Calculate days, hours, and minutes
    days = time_difference.days
    year = current_time.year - timestamp.year
    timestamp = timestamp.replace(tzinfo=from_zone)
    local_time = timestamp.astimezone(to_zone)
    if year > 0:
        return f"{local_time.strftime('%b %-d, %Y %-I:%M %p')} "

    elif days > 0:
        return f"{timestamp.strftime('%b %-d %-I:%M %p')} "
    else:
        return f"{local_time.strftime('%-I:%M %p')} "
