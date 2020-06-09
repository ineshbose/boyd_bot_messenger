import requests, pytz
from datetime import datetime
from icalendar import Calendar
from dateutil.parser import parse as dtparse


tmzn = pytz.timezone("UTC")
cal_url = "https://frontdoor.spa.gla.ac.uk/spacett/download/uogtimetable.ics"
req = {}
calendars = {}


def login(uid, pw):
    req[uid] = requests.get(cal_url, auth=(uid, pw))

    try:
        calendars[uid] = Calendar.from_ical(req[uid].content)
        return True
    except (ValueError, Exception):
        return False


def format_event(event):
    return "📝 {}\n🕘 {} - {}\n📅 {}\n📌 {}\n".format(
        event["summary"].split(")")[0] + ")"
        if "(" in event["summary"]
        else event["summary"],
        event["dtstart"].dt.strftime("%I:%M%p"),
        event["dtend"].dt.strftime("%I:%M%p"),
        event["dtstart"].dt.strftime("%d %B %Y (%A)"),
        event["location"],
    )


def read(uid, start_date=None, end_date=None):

    date1 = (
        dtparse(start_date).replace(tzinfo=tmzn)
        if start_date
        else datetime.now(tz=tmzn)
    )
    date2 = (
        dtparse(end_date).replace(tzinfo=tmzn)
        if end_date
        else date1.replace(hour=23, minute=59, second=59)
    )
    class_list = []

    for event in calendars[uid].walk("vevent"):
        if event["dtstart"].dt >= date1 and event["dtend"].dt <= date2:
            class_list.append(format_event(event))
            if not start_date:
                break

    if not class_list:
        return "There seem to be no classes. :D"

    message = "You have..\n\n" + ("\n".join(class_list))
    return (
        message
        if len(message) < 2000
        else [
            "\n".join(li)
            for li in [class_list[i : i + 10] for i in range(0, len(class_list), 10)]
        ]
    )


def check_loggedIn(uid):
    return True if uid in calendars.keys() else False
