import pytz
import requests
from datetime import datetime
from icalendar import Calendar
from dateutil.parser import parse as dtparse

try:
    from rapidfuzz import fuzz
except ImportError:
    from fuzzywuzzy import fuzz


class Timetable:
    """
    Contains methods and attributes to fetch
    and handle timetable for multiple users.
    """

    calendars = {}

    def __init__(self, cal_url, tmzn):
        self.cal_url = cal_url
        self.tmzn = pytz.timezone(tmzn)
        self.fuzz_threshold = 45
        self.msg_char_limit = 2000
        self.classes_per_msg = 10

    def login(self, uid, uni_id, uni_pw):
        try:
            self.calendars[uid] = Calendar.from_ical(
                requests.get(self.cal_url, auth=(uni_id, uni_pw)).content
            )
            return True, "Success"
        except ValueError:
            return False, "Invalid credentials."
        except Exception as e:
            return False, f"Something went wrong. Try again. {str(e)}"

    def format_event(self, event):
        return (
            f'📝 {"".join(event["summary"].partition(")")[:2])}\n'
            f'🕘 {event["dtstart"].dt.astimezone(self.tmzn).strftime("%I:%M%p")}'
            f' - {event["dtend"].dt.astimezone(self.tmzn).strftime("%I:%M%p")}\n'
            f'📅 {event["dtstart"].dt.strftime("%d %B %Y (%A)")}\n'
            f'📌 {event.get("location", "No Location Found")}\n'
        )

    def read(self, uid, start_date=None, end_date=None, class_name=None):

        if class_name and not isinstance(class_name, list):
            class_name = [class_name]

        class_list = [
            self.format_event(event)
            for event in self.iterate(uid, start_date, end_date, class_name)
        ] if start_date else [
            self.format_event(event)
            for event in self.get_one(uid, class_name)
        ]

        if not class_list:
            return ["There seem to be no classes. :D"]

        message = "\n".join(class_list)
        return (
            [message]
            if len(message) < self.msg_char_limit
            else [
                "\n".join(li)
                for li in [
                    class_list[i : i + self.classes_per_msg]
                    for i in range(0, len(class_list), self.classes_per_msg)
                ]
            ]
        )

    def get_one(self, uid, class_name=None):

        date1 = datetime.now(tz=self.tmzn)
        class_list = []

        if not class_name:
            for event in self.calendars[uid].walk("vevent"):
                if event["dtstart"].dt.astimezone(self.tmzn) >= date1:
                    class_list.append(event)
                    break

        else:
            for c_name in class_name:
                for event in self.calendars[uid].walk("vevent"):
                    if (
                        event["dtstart"].dt.astimezone(self.tmzn) >= date1
                        and fuzz.token_set_ratio(
                            c_name.lower(), event["summary"].lower()
                        ) > self.fuzz_threshold
                    ):
                        class_list.append(event)
                        break

        return class_list

    def iterate(self, uid, start_date=None, end_date=None, class_name=None):

        date1 = (
            self.tmzn.localize(dtparse(start_date).replace(tzinfo=None))
            if start_date
            else datetime.now(tz=self.tmzn)
        )
        date2 = (
            self.tmzn.localize(dtparse(end_date).replace(tzinfo=None))
            if end_date
            else date1.replace(hour=23, minute=59, second=59)
        )

        class_list = []

        for event in self.calendars[uid].walk("vevent"):
            if (
                event["dtstart"].dt.astimezone(self.tmzn) >= date1
                and event["dtstart"].dt.astimezone(self.tmzn) <= date2
            ):

                _ = (
                    class_list.extend(
                        event
                        for c_name in class_name
                        if fuzz.token_set_ratio(
                            c_name.lower(), event["summary"].lower()
                        )
                        > self.fuzz_threshold
                    )
                    if class_name
                    else class_list.append(event)
                )

        return class_list

    def check_loggedIn(self, uid):
        return uid in self.calendars
