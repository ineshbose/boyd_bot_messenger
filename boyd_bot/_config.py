# flake8: noqa
# fmt: off

app_url = ''

config = {
    # URL root for the app
    "URL_ROOT": "/",

    # timetable Configurations
    "TIMETABLE": {

        "CAL_URL": (
            "https://frontdoor.spa.gla.ac.uk/spacett/download/uogtimetable.ics"
        ),

        "TIMEZONE": "Europe/London",  # timezone

        "FUZZ_THRESHOLD": 45,  # minimum match value

        "NO_CLASS_MSG": "There seem to be no classes. :D",  # no classes message

    },

    # template Option
    "TEMPLATES": {

        "REG_FORM": "uni_theme_reg.html",  # uni_theme or default

        "MESSAGES": {

            "SUCCESS_MSG": (
                "Login successful! "
                "You can now close this page and chat to the bot."
            ),

            "HELP_TEXT": (
                "Thank you for registering. "
                "Hopefully it won't be difficult to use the bot. "
                "You can ask questions like 'what classes do I have tomorrow?', "
                "'psychology classes this year', 'next saturday 1pm'."
            ),

        },

    },

    # features you can switch on/off
    "FEATURES": {

        # read https://github.com/ineshbose/boyd_bot_messenger/issues/8
        "ONE_TIME_USE": True,

        # works for chatbots without platform user-accounts for demos
        "DEMO": True,

        # read https://github.com/ineshbose/boyd_bot_messenger/issues/3
        "SCHEDULER": False,

    },

    # simple string messages that can be replaced
    "MSG": {

        "NEW_USER": lambda name, reg_id: (
            f"Hey there, {name}! "
            "I'm Boyd Bot - your university chatbot, here to make things easier. "
            f"To get started, register here: {app_url}/register/{reg_id}"
        ),

        "NOT_REG": lambda reg_id: (
            "It doesn't seem like you've registered yet.\n"
            f"Register here: {app_url}/register/{reg_id}"
        ),

        "ERROR_LOGIN": lambda reg_id: (
            "Whoops! Something went wrong; maybe your login details changed?\n"
            f"Register here: {app_url}/register/{reg_id}"
        ),

        "REG_ACKNOWLEDGE": "Alrighty! We can get started. :D",

        "ONE_TIME_DONE": (
            "You were logged out and since we don't have your credentials, "
            "you'll have to register again!"
        ),

        "ERROR_MSG": "I'm sorry, something went wrong understanding that. :(",

    },

    # parser messages
    "PARSER": {

        "HELP_TEXT": (
            "I'm your university chatbot, so you can ask me "
            "(almost) anything regarding your timetable!\n"
            "For example, 'classes today', 'do I have psychology tomorrow?', "
            "'march 3rd'.\n\nIf you want, you can stop using my help and "
            "have your data deleted by saying 'delete data' "
            "but I don't want you to go! You'll always be welcome back. :)"
        ),

        "DELETE_SUCCESS": "Deleted! :)",

        "DELETE_FAIL": "Something went wrong. :(",

        "INTENT_UNAVAIL": "Sorry, I would not be able to do that. :("

    },

    # scheduler
    "SCHEDULER": {

        "TIMEZONE": "Europe/London",

        "UNI_MONTHS": "09-11,1-3",  # When university is on

        "UNI_DAYS": "mon-fri",  # Weekdays

        "UNI_HOURS": "7-20",  # Best to avoid night-time

        "MORNING_TEXT": lambda name, date, schedule: (
            f'Morning, {name}! '
            f'Today is {date} '
            f"and your schedule is..\n\n{schedule}"
        ),

        "REMINDER_TEXT": lambda name, event: (
            f'Hey {name}! '
            f"Hope you're on your way to\n\n{event}"
        ),

    },

    # simple logging messages that can be replaced
    "LOG": {

        "FORMAT": (
            "\033[94m[%(asctime)s] %(levelname)s in %(name)s:"
            "\033[96m %(message)s\033[0m"
        ),

        "INVALID_USER": lambda sender_id: f"{sender_id} is not a valid user",

        "USER_AUTH": lambda uid, login_result: (
            f"{uid} undergoing registration. Result: {login_result}"
        ),

        "RELOGIN": lambda uid: f"{uid} logging in again.",

        "AUTH_FAIL": lambda uid, login_result: (
            f"{uid} failed to log in. Result: {login_result}"
        ),

        "ERROR": lambda e_name, e_msg, uid, r_data: (
            f"Exception ({e_name}) thrown: {e_msg}. {uid} requested '{r_data}'."
        ),

    }
}
