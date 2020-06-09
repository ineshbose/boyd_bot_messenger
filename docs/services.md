# [services.py](https://github.com/ineshbose/boyd_bot_messenger/blob/master/services.py)
This script separates all External Services from `app.py` to declutter and make it easily replacable.


## Packages Used
* [requests](https://github.com/psf/requests)
* [pymongo](https://github.com/mongodb/mongo-python-driver)


## [Facebook Messenger](https://developers.facebook.com/products/messenger/)
Implemented in `class Facebook`.


### `send_message()`
```python
def send_message(uid, message):
    """Sends message to a user on Facebook

    Using Facebook Send API, it creates a POST request that sends a message.

    Parameters
    ----------
    uid : str
        The username / unique ID of the user.
    access_token : str
        Page Access Token of Facebook Page
    message : str
        Message to send
    
    Returns
    -------
    response
        Request status (200/400)
    """
    data = {
        "messaging_type": "RESPONSE",
        "recipient": {
            "id": uid
        },
        "message": {
            "text": message
        }
    }
    
    return requests.post("https://graph.facebook.com/v7.0/me/messages?access_token={}".format(self.access_token), json=data)
```



### `verify()`
```python
def verify(uid):
    """Verifies that the user is a Facebook User.

    Using Facebook Graph API, it creates a GET request that retrieves profile data.

    Parameters
    ----------
    uid : str
        The username / unique ID of the user.
    access_token : str
        Page Access Token of Facebook Page

    Returns
    -------
    dict
        User data as a dictionary
    """
    req = requests.get("https://graph.facebook.com/v7.0/{}?access_token={}".format(uid, self.access_token))
    return req.json()
```



## [mongoDB](https://www.mongodb.com/)
Implemented in `class Mongo`. This enables mongoDB to be easily replacable (with say `Redis`).
Most functions are one-liners and easily explainable through their names.




## [Dialogflow](https://dialogflow.com/)
Implemented in `class Dialogflow`. This function, however, doesn"t use any features of Dialogflow but handles intents externally to declutter `app.py`.

### `get_id()`
```python
def get_id(self, data):
    try:
        return data["key-to-id"]
    except KeyError:
        return None
```

### `read_next()`
```python
def read_next(self, uid, data):
    return timetable.read_schedule(uid)
```

### `read_timetable()`
```python
def read_timetable(self, uid, data):
    param = data["queryResult"]["parameters"]["date-time"]

    param_link = {
        "date_time": lambda: (param["date_time"],),
        "startDateTime": lambda: (param["startDateTime"], param["endDateTime"]),
        "startDate": lambda: (param["startDate"], param["endDate"]),
        "startTime": lambda: (param["startTime"], param["endTime"]),
        "default": lambda: ((param[:10]+"T00:00:00"+param[19:len(param)]),),
    }

    return timetable.read_schedule(uid, *(param_link.get(next(iter(param)), param_link["default"])()))
```


### `prepare_json()`
```python
def prepare_json(message):
    """Prepares a formatted JSON containing the message.

    To return a message from a POST request, Dialogflow requires a formatted JSON.

    Parameters
    ----------
    message : str
        The message to return.

    Returns
    -------
    json
        A formatted JSON for Dialogflow with the message.
    """

    res = { "fulfillmentText": message, }   # May vary(?)
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers["Content-Type"] = "application/json"
    return r
```