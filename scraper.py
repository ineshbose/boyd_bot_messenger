import requests, datetime, pytz
from icalendar import Calendar
from dateutil.parser import parse as dtparse


## Global Scopes & Constants
tmzn = pytz.timezone('Europe/London')                                   # Used to localize time and compare datetimes
cal_url = "frontdoor.spa.gla.ac.uk/spacett/download/uogtimetable.ics"   # This can be changed to any university's URL
req = {}                                                                # Requests as dictionaries to fetch ICS
calendars = {}                                                          # Calendars as dictionaries corresponding to UID
###


def login(uid, pw):
    """Logins in user with the provided credentials.

    A request fetches content from a URL with authentication, and `icalendar.Calendar` creates a calendar from that content.
    If the operation was successful, the user was successfully logged in. If not, `icalendar.Calendar` throws an exception
    since the content was not suitable to create a calendar which means the credentials were unable to fetch content through
    the request; therefore the login was unsuccessful.

    Parameters
    ----------
    uid : str
        The username / unique ID of the user for the portal.
    pw : str
        The password of the user for the portal.

    Returns
    -------
    bool
        A boolean value corresponding if the login was successful (true) or not (false).
    """
    req[uid] = requests.get("https://{}:{}@{}".format(uid,pw,cal_url))
    try:
        calendars[uid] = Calendar.from_ical(req[uid].content)
        req[uid].close()
        return True
    except Exception:
        req[uid].close()
        return False


def format_event(event):
    """Formats calendar event in a presentable string.

    The events in `icalendar.Calendar` are in the form of a dictionary. This function creates a string containing all
    necessary details about the event in a readable manner (example: `datetime` is not readable) and returns it.

    Note: The formatting is according to how event conventions are for the University of Glasgow. For example, usually events
    are titled something like "OOSE2 (Laboratory) OOSE2 LB01" or "Computing Science - 1S (Lecture) CS1S Lecture.", therefore
    the unnecessary / repetitive words after "(Laboratory)" or "(Lecture)" are removed.

    Parameters
    ----------
    event :
        An event in icalendar.Calendar['vevent'].

    Returns
    -------
    str
        A formatted, readable string for the event.
    """
    return event['summary'].split(')')[0]+')\nfrom '  + event['dtstart'].dt.strftime('%I:%M%p') + ' to ' + event['dtend'].dt.strftime('%I:%M%p') + '\nat ' \
        + event['location'] + '.\n\n' if '(' in event['summary'] else event['summary']+'\nfrom '  + event['dtstart'].dt.strftime('%I:%M%p') + ' to ' \
            + event['dtend'].dt.strftime('%I:%M%p') + '\nat ' + event['location'] + '.\n\n'


def read_date(uid, date_entry=None):
    """Fetches events for a specific date.

    Iterates through all events in the calendar and returns events that start and end between the beginning of that
    date (00:00) and end of that date (23:59).

    Parameters
    ----------
    uid : str
        The username / unique ID of the user to correspond with the calendar.
    date_entry : str
        Datetime entry from Dialogflow.

    Returns
    -------
    str
        A formatted message containing information about the events on that date.
    """
    date1 = dtparse(date_entry).replace(hour=0, minute=0, second=0, tzinfo=tmzn) if date_entry!=None else tmzn.localize(datetime.datetime.now())
    date2 = date1.replace(hour=23, minute=59, second=59, tzinfo=tmzn)
    message = "You have..\n\n"
    
    for event in calendars[uid].walk('vevent'):
        if event['dtstart'].dt > date1 and event['dtend'].dt < date2:
            message+=format_event(event)
            if date_entry == None: break

    return message if message!="You have..\n\n" else "There seem to be no classes. :D"


def check_loggedIn(uid):
    """Checks that calendar exists for the user.

    This function enables integrity and checks if a `icalendar.Calendar` exists for a specific user. If not,
    the user is logged in again in the background.

    Parameters
    ----------
    uid : str
        The username / unique ID of the user to correspond with the calendar.

    Returns
    -------
    bool
        A boolean value corresponding if the calendar exists (true) or not (false).
    """
    return True if uid in calendars.keys() else False


def send_message(uid, access_token, message):
    """Sends message to a user on Facebook

    Using Facebook Send API, it creates a POST request that sends a message.
    This function is a part of this file since it deals with requests more than `app.py`.

    Parameters
    ----------
    uid : str
        The username / unique ID of the user.
    access_token : str
        Page Access Token of Facebook Page
    message : str
        Message to send
    
    Returns
    -------
    response
        Request status (200/400)
    """
    data = {
        "messaging_type": "RESPONSE",
        "recipient": {
            "id": uid
        },
        "message": {
            "text": message
        }
    }
    
    return requests.post('https://graph.facebook.com/v7.0/me/messages?access_token={}'.format(access_token), json=data)