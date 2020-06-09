# [app.py](https://github.com/ineshbose/boyd_bot_messenger/blob/master/app.py)

This script is the Flask app. It is the only script to have access to the keys and enables webhook.


## Packages Used
* [flask](https://github.com/pallets/flask)
* [cryptography](https://github.com/pyca/cryptography)


```python
# Flask App Properties
app = Flask(__name__)
## Link views.py to app
app.register_blueprint(pages)
## Enable logging despite debug = False
app.logger.setLevel(logging.DEBUG)
## Disable logging for POST / GET status
logging.getLogger("werkzeug").setLevel(logging.ERROR)

# App URL as variable to easily change it
app_url = os.environ["APP_URL"]

# Flask Secret Key to enable FlaskForm
app.config["SECRET_KEY"] = os.environ["FLASK_KEY"]

# Webhook Token for GET request
webhook_token = os.environ["VERIFY_TOKEN"]

# Webhook Argument Name
wb_arg_name = os.environ["WB_ARG_NAME"]

# Facebook Page Access Token to use Send/Graph API
facebook = Facebook(os.environ["PAGE_ACCESS_TOKEN"])

# MongoDB data
db = Mongo(os.environ["MONGO_TOKEN"], os.environ["FIRST_CLUSTER"],
            os.environ["COLLECTION_NAME"], os.environ["WAIT_ID"])

# Initialize class Dialogflow
df = Dialogflow()

# Encryption key using Fernet
f = Fernet(os.environ["FERNET_KEY"])
```



## `webhook()`
```python
@app.route("/webhook", methods=["GET","POST"])
def webhook():
    """Enables webhook for the app.

    A method to handle POST requests with the app from Dialogflow.
    
    Returns
    -------
    json
        The response to POST request.
    """

    if request.method == "GET":
        # GET method has no use
        return redirect("/")

    # This is to enable authorisation of POST requests
    if not request.headers.get(wb_arg_name) == webhook_token:
        return "Verification token mismatch", 403

    data = request.get_json()
    sender_id = df.get_id()
    # rest of the code
    return prepare_json(response)
```



## `new_user_registration()`
```python
@app.route("/register", methods=["GET", "POST"])
def new_user_registration():
    """Registration for a new user.

    Using `wait_id`, in-registration user is distinguished and then logged in using `timetable.login()` and depending
    on returned boolean value, the page is re-rendered.

    Returns
    -------
    template
        Depending on login, the page is rendered again.
    """
    
    if request.method == "GET":
        # render template if URL argument found in database
    else:
        # try login
        facebook.send_message(fb_id, "Alrighty! We can get started. :D")    # To alert user on Facebook Messenger. This can be removed.
        return
```



## `handle_intent()`
```python
def handle_intent(data, r):
    """Checks intent for a message and creates response.

    If an intent is found in a message, a response is returned.
    Put all intents handled by the app here.

    Parameters
    ----------
    data :
        The JSON of the POST request.
    r :
        The details of the user on Mongo.

    Returns
    -------
    str
        The response if intent is satisfied

    null
        If intent is not handled by the app, Dialogflow creates response.
    """

    try:
        # if intent1: return something
        # elif intent2: return something else
        # else:
        return
    except:
        # return exception message
```



## `parse_message()`
```python
def parse_message(data, uid):
    """Parses the message of the user.

    The main method handling log in and intents for the message.

    Parameters
    ----------
    data :
        The JSON of the POST request.
    uid : str
        The unique ID for the Facebook user of the app.

    Returns
    -------
    str
        A response for the message.

    null
        If intent is not handled by app, the response is created by Dialogflow.
    """
   
    if not timetable.check_loggedIn(r["uni_id"]):
        # login
    
        if not login_result:
            # login failed
    
    return handle_intent(data, r)
```



## `log()`
```python
def log(message):
    """Logs details onto the terminal of server using Flask.

    This function can be changed to how logging is intended.

    Parameters
    ----------
    message : str
        The message to log.
    """
    app.logger.info(message)
```