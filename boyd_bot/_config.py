from . import app


# Simple string messages that can be replaced
app.config["MSG"] = {
    "REG_ACKNOWLEDGE": "Alrighty! We can get started. :D",
    "SUCCESS_MSG": "Login successful! You can now close this page and chat to the bot.",
    "ONE_TIME_DONE": "You were logged out and since we don't have your credentials, you'll have to register again!",
    "ERROR_MSG": "I'm sorry, something went wrong understanding that. :(",
}


# Features you can switch on/off
app.config["FEATURES"] = {
    "ONE_TIME_USE": True,
}
