import requests, datetime, pytz
from icalendar import Calendar


## Global Scopes
tmzn = pytz.timezone('Europe/London')                                   # Used to localize time and compare datetimes
cal_url = "frontdoor.spa.gla.ac.uk/spacett/download/uogtimetable.ics"   # This can be changed to any university's URL
req = {}                                                                # Requests as dictionaries to fetch ICS
calendars = {}                                                          # Calendars as dictionaries corresponding to UID
###


def login(uid,pw):  
    req[uid] = requests.get("https://{}:{}@{}".format(uid,pw,cal_url))
    try:
        calendars[uid] = Calendar.from_ical(req[uid].content)
        req[uid].close()
        return 1
    except:
        req[uid].close()
        return 2


def format_event(event):
    return event['summary'].split(')')[0]+')\nfrom '  + event['dtstart'].dt.strftime('%I:%M%p') + ' to ' + event['dtend'].dt.strftime('%I:%M%p') + '\nat ' + event['location'] + '.\n\n' if '(' in event['summary'] else event['summary']+'\nfrom '  + event['dtstart'].dt.strftime('%I:%M%p') + ' to ' + event['dtend'].dt.strftime('%I:%M%p') + '\nat ' + event['location'] + '.\n\n'


def read_date(date_entry, uid):
    year, month, day = map(int, date_entry.split('-'))
    date1 = datetime.datetime(year, month, day)
    date2 = date1 + datetime.timedelta(days=1)
    message = "You have..\n\n"
    
    for event in calendars[uid].walk('vevent'):
        if event['dtstart'].dt > tmzn.localize(date1) and event['dtend'].dt < tmzn.localize(date2):
            message+=format_event(event)

    return "There seem to be no classes." if message == "You have..\n\n" else message


def read_now(uid):
    message = "Up next, you have..\n\n"
    date1 = datetime.datetime.now()
    date2 = date1 + datetime.timedelta(days=1)
    
    for event in calendars[uid].walk('vevent'):
        if event['dtstart'].dt > tmzn.localize(date1) and event['dtend'].dt < tmzn.localize(date2):
            message+=format_event(event)
            break
    
    return "No class! :D" if message == "Up next, you have..\n\n" else message

def check_loggedIn(uid):
    return True if uid in calendars.keys() else False
