# flake8: noqa
# fmt: off

from . import app, app_url


# URL root for the app
app.config["URL_ROOT"] = "/"


# Template Option
app.config["TEMPLATES"] = {
    "REG_FORM": "uni_theme_reg.html",  # uni_theme or default
}


# Features you can switch on/off
app.config["FEATURES"] = {

    # read https://github.com/ineshbose/boyd_bot_messenger/issues/8
    "ONE_TIME_USE": True,

    # Works for chatbots without platform user-accounts for demos
    "DEMO": True,

    # read https://github.com/ineshbose/boyd_bot_messenger/issues/3
    "SCHEDULER": True,

}


# Simple string messages that can be replaced
app.config["MSG"] = {

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

    "SUCCESS_MSG": (
        "Login successful! "
        "You can now close this page and chat to the bot."
    ),

    "ONE_TIME_DONE": (
        "You were logged out and since we don't have your credentials, "
        "you'll have to register again!"
    ),

    "ERROR_MSG": "I'm sorry, something went wrong understanding that. :(",

}


# Simple logging messages that can be replaced
app.config["LOG"] = {

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

# fmt: on

config = app.config