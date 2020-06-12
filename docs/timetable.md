# [`timetable.py`](https://github.com/ineshbose/boyd_bot_messenger/blob/master/timetable.py)

This script handles going through the timetables.


## Packages Used

* [icalendar](https://github.com/collective/icalendar)
* [requests](https://github.com/psf/requests)
* [pytz](https://github.com/stub42/pytz)
* [dateutil](https://github.com/dateutil/dateutil)


## Setup

The script is initialized using the following lines.

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



## `login(uid, pw)`

Logins in user with the provided credentials. <br>
A request fetches content from a URL with authentication, and `icalendar.Calendar` creates a calendar from that content. If the operation was successful, the user was successfully logged in. If not, `icalendar.Calendar` throws an exception since the content was not suitable to create a calendar which means the credentials were unable to fetch content through the request; therefore the login was unsuccessful.

```python
>>> login("123456Z", "password123")
False
APP: 1234567890 undergoing registration. Result: False
```

|                                       Parameters                                          |           Returns            |
|-------------------------------------------------------------------------------------------|------------------------------|
| **`uid`:** the university ID of the user<br>**`pw`:** the university password of the user | **`bool`:** the login result |



## `format_event(event)`

Formats calendar event in a presentable string. <br>
The events in `icalendar.Calendar` are in the form of a dictionary. This function creates a string containing all necessary details about the event in a readable manner (example: `datetime` is not readable) and returns it. <br>
**Note:** The formatting is according to how event conventions are for the University of Glasgow. For example, usually events are titled something like "OOSE2 (Laboratory) OOSE2 LB01" or "Computing Science - 1S (Lecture) CS1S Lecture.", therefore the unnecessary / repetitive words after "(Laboratory)" or "(Lecture)" are removed.

```sh
>>> format_event({"summary": "Python Tutorial", "dtstart": <20050404T080000Z>, 
                  "dtend": <20050404T090000Z>, "location": "Boyd Orr Building"})
📝 Python Tutorial
🕘 08:00AM - 09:00AM
📅 04 April 2005 (Monday)
📌 Boyd Orr Building
```

|                       Parameters                      |                    Returns                      |
|-------------------------------------------------------|-------------------------------------------------|
| **`event`:** the `icalendar.Calendar.event` to format | **`str`:** a string representation of the event |



## `read_schedule(uid, start_date=None, end_date=None)`

Iterates through all events in the calendar and returns events that start and end between the beginning of that date (00:00) and end of that date (23:59).

```sh
>>> read_schedule("123456Z", start_date="20050404T080000+01:00")
You have..

📝 Python Tutorial
🕘 08:00AM - 09:00AM
📅 04 April 2005 (Monday)
📌 Boyd Orr Building
```

|                                                                       Parameters                                                                         |                                    Returns                                                                     |
|----------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------|
| **`uid`:** the university ID of the user<br>**`start_date`:** `date-time` start parameter if found<br>**`end_date`:** `date-time` end parameter if found | **`str`:** the timetable as a message<br>**`list`:** list of strings if message character limit is passed |



## `check_loggedIn(uid)`

Checks that calendar exists for the user. This function enables integrity and checks if a `icalendar.Calendar` exists for a specific user. It not, the user is logged in again the background.

```python
>>> check_loggedIn("123456Z")
True
```

|                 Parameters              |                 Returns                 |
|-----------------------------------------|-----------------------------------------|
| **`uid`:** the university ID of the user| **`bool`:** if user's calendar is found |