from datetime import datetime
from dateutil import tz


def time_ago_message(timestamp):
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

    elif days > 0 or current_time.day != local_time.day:
        return f"{timestamp.strftime('%b %-d %-I:%M %p')} "
    else:
        return f"{local_time.strftime('%-I:%M %p')} "


def time_ago(timestamp):
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()

    current_time = datetime.utcnow()
    time_difference = current_time - timestamp
    # Calculate days, hours, and minutes
    days = time_difference.days
    hours, remainder = divmod(time_difference.seconds, 3600)
    minutes, _ = divmod(remainder, 60)

    year = current_time.year - timestamp.year
    timestamp = timestamp.replace(tzinfo=from_zone)
    local_time = timestamp.astimezone(to_zone)
    if year > 0:
        return f"{local_time.strftime('%b %-d, %Y %-I:%M %p')} "
    elif days > 2:
        return f"{timestamp.strftime('%b %-d %-I:%M %p')} "
    elif days > 0 and days < 2:
        return f"{days} {'day' if days == 1 else 'days'} ago"
    elif hours > 0:
        return f"{hours} {'hour' if hours == 1 else 'hours'} ago"
    elif minutes > 0:
        return f"{minutes} {'minute' if minutes == 1 else 'minutes'} ago"
    elif minutes == 0:
        return "Just now"
    else:
        return f"{local_time.strftime('%-I:%M %p')} "
