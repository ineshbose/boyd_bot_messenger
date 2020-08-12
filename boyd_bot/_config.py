from . import app


# URL root for the app
app.config["URL_ROOT"] = "/"


# Template Option
app.config["TEMPLATES"] = {
    "REG_FORM": "uni_theme_reg.html",  # uni_theme or default
}


# Simple string messages that can be replaced
app.config["MSG"] = {
    "REG_ACKNOWLEDGE": "Alrighty! We can get started. :D",
    "SUCCESS_MSG": "Login successful! You can now close this page and chat to the bot.",
    "ONE_TIME_DONE": "You were logged out and since we don't have your credentials, you'll have to register again!",
    "ERROR_MSG": "I'm sorry, something went wrong understanding that. :(",
}


# Features you can switch on/off
app.config["FEATURES"] = {
    "ONE_TIME_USE": True,  # On-going issue (read https://github.com/ineshbose/boyd_bot_messenger/issues/8)
    "DEMO": True,  # Works for chatbots without platform user-accounts (eg Dialogflow Web Demo / Embedded)
    "SCHEDULER": {  # Background processing (read https://github.com/ineshbose/boyd_bot_messenger/issues/3)
        "SERVER": True,  # If your hosting service needs to run scheduler separately
        "APP": False,  # If you can run scheduler along with app (no down-time)
    },
}
