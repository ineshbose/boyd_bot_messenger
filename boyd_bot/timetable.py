import requests, pytz
from datetime import datetime
from rapidfuzz import fuzz
from icalendar import Calendar
from dateutil.parser import parse as dtparse


class Timetable:
    calendars = {}

    def __init__(
        self,
        cal_url,
        tmzn="UTC",
        fuzz_threshold=36,
        msg_char_limit=2000,
        classes_per_msg=10,
    ):
        self.cal_url = cal_url
        self.tmzn = pytz.timezone(tmzn)
        self.fuzz_threshold = fuzz_threshold
        self.msg_char_limit = msg_char_limit
        self.classes_per_msg = classes_per_msg

    def login(self, uid, uni_id, uni_pw):
        try:
            self.calendars[uid] = Calendar.from_ical(
                requests.get(self.cal_url, auth=(uni_id, uni_pw)).content
            )
            return True, "Success"
        except ValueError:
            return False, "Invalid credentials."
        except Exception as e:
            return False, "Something went wrong. Try again. {}".format(e.__str__())

    def format_event(self, event):
        return "📝 {}\n🕘 {} - {}\n📅 {}\n📌 {}\n".format(
            event["summary"].split(")")[0] + ")"
            if "(" in event["summary"]
            else event["summary"],
            event["dtstart"].dt.strftime("%I:%M%p"),
            event["dtend"].dt.strftime("%I:%M%p"),
            event["dtstart"].dt.strftime("%d %B %Y (%A)"),
            event.get("location", "No Location Found"),
        )

    def jsonify_desc(self, event):
        return (
            dict(
                (k.strip(), v.strip())
                for k, v in (
                    item.split(":") for item in event["description"].splitlines()
                )
            )
            if "description" in event
            else None
        )

    def read(self, uid, start_date=None, end_date=None, class_name=None):
        class_list = self.iterate(uid, start_date, end_date, class_name)

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

    def iterate(self, uid, start_date=None, end_date=None, class_name=None):

        date1 = (
            dtparse(start_date).replace(tzinfo=self.tmzn)
            if start_date
            else datetime.now(tz=self.tmzn)
        )
        date2 = (
            dtparse(end_date).replace(tzinfo=self.tmzn)
            if end_date
            else date1.replace(hour=23, minute=59, second=59)
        )
        class_list = []

        for event in self.calendars[uid].walk("vevent"):
            if event["dtstart"].dt >= date1 and event["dtend"].dt <= date2:

                if not start_date:
                    class_list.append(self.format_event(event))
                    break

                if class_name:
                    class_name = (
                        [class_name] if not isinstance(class_name, list) else class_name
                    )
                    for c_name in class_name:
                        if (
                            fuzz.token_set_ratio(
                                c_name.lower(), event["summary"].lower()
                            )
                            > self.fuzz_threshold
                        ):
                            class_list.append(self.format_event(event))

                else:
                    class_list.append(self.format_event(event))

        return class_list

    def check_loggedIn(self, uid):
        print(self.calendars.keys())
        return True if uid in self.calendars else False
