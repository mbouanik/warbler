from datetime import datetime
from dateutil import tz
from os import getenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


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
        return f"{local_time.strftime('%-I:%M %p')}"


def welcome_email(reciever, name):
    print(getenv("SENDGRID_API_KEY"))
    message = Mail(
        from_email="contact@warp.com",
        to_emails=reciever,
        subject="Welcome To Warp",
        html_content=f"<h1> Welcome to Warp {name}</h1> <br> <p> Thank you {name} for signing up take the convesation beyond </p>",
    )
    try:
        sg = SendGridAPIClient(getenv("SENDGRID_API_KEY"))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)
