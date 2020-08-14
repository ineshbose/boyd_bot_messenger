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
                for msg in timetable.read(uid, time1, time2):
                    msg = "Hey, {}! Hope you're on your way to\n{}".format(
                        platform.get_user_data(uid).get("first_name", "heads up"), msg
                    )
                    platform.send_message(uid, msg)

    def morning_alert(self):
        """
        Job to send users their schedule in the morning.
        """
        for data in db.get_all():
            uid = data["_id"]
            if data.get("subscribe") and (
                timetable.check_loggedIn(uid)
                or timetable.login(uid, data["uni_id"], data["uni_pw"])[0]
            ):
                for msg_no, msg in enumerate(
                    timetable.read(uid, datetime.now().isoformat())
                ):
                    if msg_no == 0:
                        msg = "Morning, {}! Today is {} and your schedule is..\n{}".format(
                            platform.get_user_data(uid).get("first_name", "sunshine"),
                            datetime.now().strftime("%d %B (%A)"),
                            msg,
                        )
                    platform.send_message(uid, msg)

    def run(self):
        """
        Starts the scheduler in the background.
        """
        self.scheduler.add_job(func=self.clear_db, trigger="cron", day="last")
        self.scheduler.add_job(
            func=self.morning_alert,
            trigger="cron",
            month="09-11,1-3",  # When university is on
            day_of_week="mon-fri",  # Weekdays
            hour="08",  # At 8AM every morning
        )
        self.scheduler.add_job(func=self.check_class, trigger="interval", minutes=10)
        self.scheduler.start()
