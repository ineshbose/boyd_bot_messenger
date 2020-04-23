import os, requests
import time, datetime, pytz
from icalendar import Calendar, Event


## Global Scopes
tmzn = pytz.timezone('Europe/London')
req = {}
calendars = {}
###


def login(guid,passw):  
    req[guid] = requests.get("https://{}:{}@frontdoor.spa.gla.ac.uk/spacett/download/uogtimetable.ics".format(guid,passw))
    try:
        calendars[guid] = Calendar.from_ical(req[guid].content)
        req[guid].close()
        return 1
    except:
        req[guid].close()
        return 2


def format_event(event):
    return event['summary'].split(')')[0]+')\nfrom '  + event['dtstart'].dt.strftime('%I:%M%p') + ' to ' + event['dtend'].dt.strftime('%I:%M%p') + '\nat ' + event['location'] + '.\n\n' if '(' in event['summary'] else event['summary']+'\nfrom '  + event['dtstart'].dt.strftime('%I:%M%p') + ' to ' + event['dtend'].dt.strftime('%I:%M%p') + '\nat ' + event['location'] + '.\n\n'


def read_date(date_entry, guid):
    year, month, day = map(int, date_entry.split('-'))
    date1 = datetime.datetime(year, month, day)
    date2 = date1 + datetime.timedelta(days=1)
    message = "You have..\n\n"
    
    for event in calendars[guid].walk('vevent'):
        if event['dtstart'].dt > tmzn.localize(date1) and event['dtend'].dt < tmzn.localize(date2):
            message+=format_event(event)

    return "There seem to be no classes." if message == "You have..\n\n" else message


def read_now(guid):
    message = "Up next, you have..\n\n"
    date1 = datetime.datetime.now()
    date2 = date1 + datetime.timedelta(days=1)
    
    for event in calendars[guid].walk('vevent'):
        if event['dtstart'].dt > tmzn.localize(date1) and event['dtend'].dt < tmzn.localize(date2):
            message+=format_event(event)
            break
    
    return "No class! :D" if message == "Up next, you have..\n\n" else message

def check_loggedIn(guid):
    return True if guid in calendars.keys() else False