# [`__init__.py`](https://github.com/ineshbose/boyd_bot_messenger/blob/master/boyd_bot/__init__.py)

This script is the app initialiser and eventually a compiler in a way since all imports are happening over here.


## Packages Used

* [flask](https://github.com/pallets/flask)


## Setup

The app is initialized using the following lines. All environment variables are loaded onto the scripts.

```python
# Flask App Properties
app = Flask(__name__)
## Link views.py to app
app.register_blueprint(pages)
## Enable logging despite debug = False
app.logger.setLevel(logging.DEBUG)
## Disable logging for POST / GET status (Not Recommended)
logging.getLogger("werkzeug").setLevel(logging.ERROR)

# App URL as variable to easily change it
app_url = os.environ["APP_URL"]

# Flask Secret Key to enable FlaskForm
app.config["SECRET_KEY"] = os.environ["FLASK_KEY"]

# Webhook Token for GET request
webhook_token = os.environ["VERIFY_TOKEN"]

# Webhook Argument Name
wb_arg_name = os.environ["WB_ARG_NAME"]

# Custom Platform API
platform = Platform(access_token=os.environ["PAGE_ACCESS_TOKEN"])

# Custom Database API
db = Database(
    cluster=os.environ["MONGO_TOKEN"],
    db=os.environ["FIRST_CLUSTER"],
    collection=os.environ["COLLECTION_NAME"],
)

# Custom Parsing API
parser = Parser()

# Custom Hasher/Cryptographer API
guard = Guard(key=os.environ["FERNET_KEY"])
```



## `log(message)`

Prints essential information on the console of the server. This helps in easily changing the process of keeping logs.

```python
>>> log("lorem ipsum")
APP: lorem ipsum
```

|                 Parameters              |    Returns  |
|-----------------------------------------|-------------|
| **`message`:** the message to log       | **`None`**  |