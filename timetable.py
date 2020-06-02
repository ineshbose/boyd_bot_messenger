import requests, datetime, pytz
from icalendar import Calendar
from dateutil.parser import parse as dtparse


tmzn = pytz.timezone('Europe/London')
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
    return event['summary'].split(')')[0]+')\nfrom '  + event['dtstart'].dt.strftime('%I:%M%p') + ' to ' + event['dtend'].dt.strftime('%I:%M%p') + '\nat ' \
        + event['location'] + '.\n\n' if '(' in event['summary'] else event['summary']+'\nfrom '  + event['dtstart'].dt.strftime('%I:%M%p') + ' to ' \
            + event['dtend'].dt.strftime('%I:%M%p') + '\nat ' + event['location'] + '.\n\n'


def read_date(uid, start_date=None, end_date=None):

    date1 = dtparse(start_date).replace(hour=0, minute=0, second=0, tzinfo=tmzn) if start_date!=None else tmzn.localize(datetime.datetime.now())
    date2 = dtparse(end_date) if end_date!=None else date1.replace(hour=23, minute=59, second=59, tzinfo=tmzn)
    message = "You have..\n\n"
    
    for event in calendars[uid].walk('vevent'):
        if event['dtstart'].dt > date1 and event['dtend'].dt < date2:
            message+=format_event(event)
            if start_date == None: break

    return message if message!="You have..\n\n" else "There seem to be no classes. :D"


def check_loggedIn(uid):
    return True if uid in calendars.keys() else False