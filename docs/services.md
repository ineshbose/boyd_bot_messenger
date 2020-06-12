# [`services.py`](https://github.com/ineshbose/boyd_bot_messenger/blob/master/services.py)

This script separates all External Services from `app.py` to declutter and make it easily replacable.


## Packages Used

* [requests](https://github.com/psf/requests)
* [pymongo](https://github.com/mongodb/mongo-python-driver)



## [Facebook Messenger](https://developers.facebook.com/products/messenger/)

Implemented in _class_ `Facebook`.


### `Facebook`.**`access_token`**

Page Access Token for the app.


### `Facebook`.**`send_message(uid, message)`**

Creates a POST request, using [Facebook Send API](), to send a message to a user on Facebook as the page.

```python
    data = {
        "messaging_type": "RESPONSE",
        "recipient": {"id": uid},
        "message": {"text": message},
    }

    return requests.post(
        "https://graph.facebook.com/v7.0/me/messages?access_token={}".format(
            self.access_token
        ),
        json=data,
    )
```

|                                       Parameters                                              |                 Returns                  |
|-----------------------------------------------------------------------------------------------|------------------------------------------|
| **`uid`:** the unique sender ID of the user<br>**`message`:** the message to send to the user | **`requests.Response`:** response status |


### `Facebook`.**`get_user_data(uid)`**

Verifies a request has been made by a Facebook user and fetches basic user information using [Facebook Graph API]().

```python
    req = requests.get(
        "https://graph.facebook.com/v7.0/{}?access_token={}".format(
            uid, self.access_token
        )
    )
    return req.json()
```

|                 Parameters                  |                 Returns                |
|---------------------------------------------|----------------------------------------|
| **`uid`:** the unique sender ID of the user | **`dict`:** information about the user |



## [mongoDB](https://www.mongodb.com/)

Implemented in _class_ `Mongo`. This enables mongoDB to be easily replacable (with say `Redis`).
Most functions are one-liners and easily explainable through their names.


### `Mongo`.**`cluster`**

Initialiser for `MongoClient()`.


### `Mongo`.**`db`**

Index specifier for database in the cluster.


### `Mongo`.**`collection`**

Index specifier for collection in the database.


### `Mongo`.**`wait_id`**

Separator between registered and in-registration users.



## [Dialogflow](https://dialogflow.com/)

Implemented in _class_ `Dialogflow`. This function, however, doesn't use any features of Dialogflow but handles intents externally to declutter `app.py`.


### `Dialogflow`.**`get_id(data)`**

Maps to unique sender ID through Dialogflow's POST request data.

|                 Parameters              |                  Returns                    |
|-----------------------------------------|---------------------------------------------|
| **`data`:** the POST request dictionary | **`str`:** the unique sender ID of the user |


### `Dialogflow`.**`delete_data(uid, db)`**

Generates response for `delete data` intent.

|                                   Parameters                                         |                    Returns                   |
|--------------------------------------------------------------------------------------|----------------------------------------------|
| **`uid`:** the unique sender ID of the user<br>**`db`:** the database to delete from | **`str`:** if deletion was successful or not |


### `Dialogflow`.**`read_next(uid)`**

Generates response for `read next` intent.

|                 Parameters              |             Returns                |
|-----------------------------------------|------------------------------------|
| **`uid`:** the university ID of the user| **`str`:** the timetable as string |


### `Dialogflow`.**`read_timetable(uid, data)`**

Generates response for `read timetable` intent. This method features a dictionary to map `date-time` parameters to arguments in order to avoid a `if-elif-...-else` ladder.

```python
    param_link = {
        "date_time": lambda: (param["date_time"],),
        "startDateTime": lambda: (param["startDateTime"], param["endDateTime"]),
        "startDate": lambda: (param["startDate"], param["endDate"]),
        "startTime": lambda: (param["startTime"], param["endTime"]),
        "default": lambda: ((param[:10]+"T00:00:00"+param[19:len(param)]),),
    }
```

|                                  Parameters                                         |                                             Returns                                            |
|-------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------|
| **`uid`:** the university ID of the user<br>**`data`:** the POST request dictionary | **`str`:** the timetable as string<br>**`list`:** if string has characters more than the limit |


### `Dialogflow`.**`prepare_json(message)`**

Prepares a formatted JSON containing the message as a response to the POST request.

```python
    res = {"fulfillmentMessages": []}

    if isinstance(message, list):
        for m in message:
            res["fulfillmentMessages"].append({"text": {"text": [m]}})
    else:
        res["fulfillmentMessages"].append({"text": {"text": [message]}})

    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers["Content-Type"] = "application/json"
    return r
```

|                                  Parameters                       |                   Returns                    |
|-------------------------------------------------------------------|----------------------------------------------|
| **`message`:** the message(s) to send as response to POST request | **`requests.response`:** the response status |