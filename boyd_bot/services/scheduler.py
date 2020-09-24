import pytz
from datetime import datetime, timedelta
from .. import db, timetable, platform
from .._config import config
from apscheduler.schedulers.background import BackgroundScheduler


class Scheduler:
    """
    Schedules certain jobs in the background.
    """

    def __init__(self):
        """
        Creating an instance of the scheduler package.
        """
        self.tmzn = pytz.timezone(config["SCHEDULER"]["TIMEZONE"])
        self.scheduler = BackgroundScheduler(timezone=self.tmzn)
        self.uni_months = config["SCHEDULER"]["UNI_MONTHS"]
        self.uni_days = config["SCHEDULER"]["UNI_DAYS"]
        self.uni_hours = config["SCHEDULER"]["UNI_HOURS"]

    def clear_db(self):
        """
        Job to clear the database once a while.
        """
        db.clear_db()

    def check_class(self):
        """
        Job to check for upcoming events and notify users.
        """
        for data in db.get_all():
            time1 = datetime.now(tz=self.tmzn).isoformat()
            time2 = (datetime.now(tz=self.tmzn) + timedelta(minutes=10)).isoformat()
            uid = data["_id"]
            if (
                ("subscribe" in data and "before_class" in data["subscribe"])
                and (
                    timetable.check_loggedIn(uid)
                    or timetable.login(uid, data["uni_id"], data["uni_pw"])[0]
                )
            ):
                _ = [
                    platform.send_message(
                        uid,
                        config["SCHEDULER"]["REMINDER_TEXT"](
                            platform.get_user_data(uid).get("first_name", " - heads up"),
                            timetable.format_event(event)
                        )
                    ) for event in timetable.iterate(uid, time1, time2)
                ]

    def morning_alert(self):
        """
        Job to send users their schedule in the morning.
        """
        time_now = datetime.now(tz=self.tmzn)
        for data in db.get_all():
            uid = data["_id"]
            if (
                ("subscribe" in data and "morning" in data["subscribe"])
                and (
                    timetable.check_loggedIn(uid)
                    or timetable.login(uid, data["uni_id"], data["uni_pw"])[0]
                    )
            ):
                platform.send_message(
                    uid,
                    config["SCHEDULER"]["MORNING_TEXT"](
                        platform.get_user_data(uid).get("first_name", "sunshine"),
                        time_now.strftime("%d %B (%A)"),
                        timetable.read(uid, time_now.isoformat())
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
