from datetime import datetime, timedelta
from .. import db, timetable, platform
from apscheduler.schedulers.background import BackgroundScheduler


class Scheduler:
    """
    Schedules certain jobs in the background.
    """

    def __init__(self):
        """
        Creating an instance of the scheduler package.
        """
        self.scheduler = BackgroundScheduler()
        self.uni_months = "09-11,1-3"  # When university is on
        self.uni_days = "mon-fri"  # Weekdays
        self.uni_hours = "7-20"  # Best to avoid night-time

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
            time1 = datetime.now().isoformat()
            time2 = (datetime.now() + timedelta(minutes=10)).isoformat()
            uid = data["_id"]
            if (
                data.get("subscribe")
                and (
                    timetable.check_loggedIn(uid)
                    or timetable.login(uid, data["uni_id"], data["uni_pw"])[0]
                )
                and timetable.iterate(uid, time1, time2)
            ):
                u_dt = platform.get_user_data(uid)
                for msg in timetable.read(uid, time1, time2):
                    msg = (
                        f'Hey {u_dt.get("first_name", " - heads up")}! '
                        f"Hope you're on your way to\n{msg}"
                    )
                    platform.send_message(uid, msg)

    def morning_alert(self):
        """
        Job to send users their schedule in the morning.
        """
        time_now = datetime.now()
        for data in db.get_all():
            uid = data["_id"]
            if data.get("subscribe") and (
                timetable.check_loggedIn(uid)
                or timetable.login(uid, data["uni_id"], data["uni_pw"])[0]
            ):
                u_dt = platform.get_user_data(uid)
                for msg_no, msg in enumerate(
                    timetable.read(uid, time_now.isoformat())
                ):
                    if msg_no == 0:
                        msg = (
                            f'Morning, {u_dt.get("first_name", "sunshine")}! '
                            f'Today is {time_now.strftime("%d %B (%A)")} '
                            f"and your schedule is..\n{msg}"
                        )
                    platform.send_message(uid, msg)

    def run(self):
        """
        Starts the scheduler in the background.
        """
        self.scheduler.add_job(
            func=self.clear_db,
            trigger="cron",
            week="*/3",  # Clear every 3 weeks
        )

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
