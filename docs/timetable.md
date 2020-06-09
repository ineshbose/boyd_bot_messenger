# [timetable.py](https://github.com/ineshbose/boyd_bot_messenger/blob/master/timetable.py)
This script handles going through the timetables.

```python
# Used to localize time and compare datetimes
tmzn = pytz.timezone("Europe/London")

# This can be changed to any university's URL
cal_url = "link/to/timetable.ics"

# Requests as dictionaries to fetch ICS
req = {}

# Calendars as dictionaries corresponding to UID
calendars = {}
```

## Packages Used
* [icalendar](https://github.com/collective/icalendar)
* [requests](https://github.com/psf/requests)
* [pytz](https://github.com/stub42/pytz)
* [dateutil](https://github.com/dateutil/dateutil)



## `login()`
```python
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
    req[uid] = requests.get(cal_url, auth=(uid, pw))
    try:
        calendars[uid] = Calendar.from_ical(req[uid].content)
        return True
    except (ValueError, Exception): ## a ValueError is raised
        return False
```



## `format_event()`
```python
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
        An event in icalendar.Calendar["vevent"].

    Returns
    -------
    str
        A formatted, readable string for the event.
    """
    return #formatted event
```



## `read_schedule()`
```python
def read_schedule(uid, start_date=None, end_date=None):
    """Fetches events for a specific date.

    Iterates through all events in the calendar and returns events that start and end between the beginning of that
    date (00:00) and end of that date (23:59).

    Parameters
    ----------
    uid : str
        The username / unique ID of the user to correspond with the calendar.
    start_date : str
        Datetime entry from Dialogflow.

    Returns
    -------
    str
        A formatted message containing information about the events on that date.
    """
    # iterate through timetable
    return message
```



## `check_loggedIn()`
```python
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
```