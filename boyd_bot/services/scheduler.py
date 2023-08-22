import pytz
from datetime import datetime, timedelta
from .._config import config
from apscheduler.schedulers.background import BackgroundScheduler


class Scheduler:
    """
    Schedules certain jobs in the background.
    """

    def __init__(self, db, timetable, platform):
        """
        Creating an instance of the scheduler package.
        """
        self.db = db
        self.timetable = timetable
        self.platform = platform

        self.tmzn = pytz.timezone(config["SCHEDULER"]["TIMEZONE"])
        self.scheduler = BackgroundScheduler(timezone=self.tmzn)
        self.uni_months = config["SCHEDULER"]["UNI_MONTHS"]
        self.uni_days = config["SCHEDULER"]["UNI_DAYS"]
        self.uni_hours = config["SCHEDULER"]["UNI_HOURS"]

    def verify(self, data, sub_type):
        return (
            ("subscribe" in data and sub_type in data["subscribe"]) and (
            self.timetable.check_loggedIn(data["_id"])
            or self.timetable.login(data["_id"], data["uni_id"], data["uni_pw"])[0]
            )
        )

    def clear_db(self):
        """
        Job to clear the database once a while.
        """
        self.db.clear_db()

    def check_class(self):
        """
        Job to check for upcoming events and notify users.
        """
        for data in self.db.get_all():
            time1 = datetime.now(tz=self.tmzn).isoformat()
            time2 = (datetime.now(tz=self.tmzn) + timedelta(minutes=10)).isoformat()
            uid = data["_id"]
            if self.verify(data, "before_class"):
                _ = [
                    self.platform.send_message(
                        uid,
                        config["SCHEDULER"]["REMINDER_TEXT"](
                            self.platform.get_user_data(uid).get("first_name", " - heads up"),
                            self.timetable.format_event(event)
                        )
                    ) for event in self.timetable.iterate(uid, time1, time2)
                ]

    def morning_alert(self):
        """
        Job to send users their schedule in the morning.
        """
        time_now = datetime.now(tz=self.tmzn)
        for data in self.db.get_all():
            uid = data["_id"]
            if self.verify(data, "morning"):
                self.platform.send_message(
                    uid,
                    config["SCHEDULER"]["MORNING_TEXT"](
                        self.platform.get_user_data(uid).get("first_name", "sunshine"),
                        time_now.strftime("%d %B (%A)"),
                        self.timetable.read(uid, time_now.isoformat())
                    ),
                )

    def run(self):
        """
        Starts the scheduler in the background.
        """

        '''
        self.scheduler.add_job(
            func=self.clear_db,
            trigger="cron",
            week="*/3",  # Clear every 3 weeks
        )
        ''' # Disabled for now

        self.scheduler.add_job(
            func=self.morning_alert,
            trigger="cron",
            month=self.uni_months,
            day_of_week=self.uni_days,
            hour="08",  # At 8AM every morning
        )

        self.scheduler.add_job(
            func=self.check_class,
            trigger="cron",
            month=self.uni_months,
            hour=self.uni_hours,
            minute="*/10",  # Every 10 minutes
        )

        self.scheduler.start()
