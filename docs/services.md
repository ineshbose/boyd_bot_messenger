# [`services.py`](https://github.com/ineshbose/boyd_bot_messenger/blob/master/services.py)

This script separates all External Services from `app.py` to declutter and make it easily replacable.


## Packages Used

* [requests](https://github.com/psf/requests)
* [pymongo](https://github.com/mongodb/mongo-python-driver)
* [cryptography](https://github.com/pyca/cryptography)




## [Facebook Messenger](https://developers.facebook.com/products/messenger/)

Implemented in _class_ `Platform`.


### `Platform`.**`access_token`**

Page Access Token for the app.


### `Platform`.**`send_message(uid, message)`**

Creates a POST request, using [Facebook Send API](https://developers.facebook.com/docs/messenger-platform/reference/send-api/), to send a message to a user on Facebook as the page.

```python
>>> from services import Platform
>>> platform = Platform("token")
>>> platform.send_message("1234567890", "Random Text")

{"error": {"message": "Invalid OAuth access token.","type": "OAuthException","code": 190,"fbtrace_id": "AGc_9nHR-ZkQ0RVDs4L59Hz"}}
```

|                                       Parameters                                              |                 Returns                  |
|-----------------------------------------------------------------------------------------------|------------------------------------------|
| **`uid`:** the unique sender ID of the user<br>**`message`:** the message to send to the user | **`requests.Response`:** response status |


### `Platform`.**`get_user_data(uid)`**

Verifies a request has been made by a Facebook user and fetches basic user information using [Facebook Graph API](https://developers.facebook.com/docs/graph-api/).

```python
>>> from services import Platform
>>> platform = Platform("token")
>>> platform.get_user_data("1234567890")

{"error": {"message": "Unsupported get request. Object with ID '1234567890' does not exist, cannot be loaded due to missing permissions, or does not support this operation. Please read the Graph API documentation at https://developers.facebook.com/docs/graph-api", "type": "GraphMethodException", "code": 100, "error_subcode": 33,}}
```

|                 Parameters                  |                 Returns                |
|---------------------------------------------|----------------------------------------|
| **`uid`:** the unique sender ID of the user | **`dict`:** information about the user |


### `Platform`.**`get_id(data)`**

Maps to unique sender ID through POST request data.

|                 Parameters              |                  Returns                    |
|-----------------------------------------|---------------------------------------------|
| **`data`:** the POST request dictionary | **`str`:** the unique sender ID of the user |


### `Platform`.**`reply(message=None, context=None)`**

Prepares a formatted JSON containing the message as a response to the POST request.

```python
>>> from services import Platform
>>> platform = Platform("token")
>>> platform.reply("Hello, developer.")
```

|                                  Parameters                       |                   Returns                    |
|-------------------------------------------------------------------|----------------------------------------------|
| **`message`:** the message(s) to send as response to POST request | **`requests.response`:** the response status |



## [mongoDB](https://www.mongodb.com/)

Implemented in _class_ `Database`. This enables mongoDB to be easily replacable (with say `Redis`).
Most functions are one-liners and easily explainable through their names.


### `Database`.**`cluster`**

Initialiser for `MongoClient()`.


### `Database`.**`db`**

Index specifier for database in the cluster.


### `Database`.**`collection`**

Index specifier for collection in the database.


### Note

A good idea to keep user-data as in JSON format with the following keys:

* `_id`: User ID (**Primary Key**)
* `uni_id`: User's University ID for login (**ENCRYPTED**)
* `uni_pass`: User's University Password for login (**ENCRYPTED**)
* `reg_id`: User's Registration ID (**SHA256 HASHED**)



## [Dialogflow](https://dialogflow.com/)

Implemented in _class_ `Parser`. This class, however, doesn't use any features of Dialogflow but handles intents externally to declutter `app.py`.


### `Parser`.**`delete_data(uid, db)`**

Generates response for `delete data` intent.

|                                   Parameters                                         |                    Returns                   |
|--------------------------------------------------------------------------------------|----------------------------------------------|
| **`uid`:** the unique sender ID of the user<br>**`db`:** the database to delete from | **`str`:** if deletion was successful or not |


### `Parser`.**`read_timetable(uid, data)`**

Generates response for `read timetable` intent. This method features a dictionary to map `date-time` (since they may vary for different services) and entities parameters to arguments in order to avoid a `if-elif-...-else` ladder.

```python
    param_keys = {
                    "date_time": ["date_time"],
                    "startDateTime": ["startDateTime", "endDateTime"],
                    "startDate": ["startDate", "endDate"],
                    "startTime": ["startTime", "endTime"],
                }
```

|                                  Parameters                                         |                        Returns                        |
|-------------------------------------------------------------------------------------|-------------------------------------------------------|
| **`uid`:** the university ID of the user<br>**`data`:** the POST request dictionary | **`list`:** schedule for days according to parameters |


## `Parser`.**`parse(uid, data, db)`**

The main method to be called for parsing. It finds intents handled by the app, calls the function and returns the response.

```python
>>> parse({"keys-to-intent": "delete data"}, "1234567890", "123456Z")
Deleted! :)
```

|                                                               Parameters                                                          |                                Returns                                   |
|-----------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------|
| **`request_data`:** the POST request dictionary<br>**`uid`:** the unique sender ID of the user<br>**`db`:** the database instance | **`str`:** the response<br>**`None`:** if response is not handled by app |



## [Cryptography](https://pypi.org/project/cryptography/)

Implemented in _class_ `Guard`. This function, however, doesn't use any features of Dialogflow but handles intents externally to declutter `app.py`.


### `Guard`.**`fernet`**

Initialiser for `Fernet()`.


### `Guard`.**`encrypt(val)`**

Encodes and encrypts `val` according to Fernet key.

|            Parameters            |             Returns            |
|----------------------------------|--------------------------------|
| **`val`:** the object to encrypt | **`binary`:** encrypted object |


### `Guard`.**`decrypt(val)`**

Decrypts and decodes `val` according to Fernet key.

|            Parameters            |           Returns           |
|----------------------------------|-----------------------------|
| **`val`:** the object to decrypt | **`str`:** decrypted object |


### `Guard`.**`sha256(val)`**

Hashes `val` using SHA-256 algorithm with `hashlib`.

|          Parameters           |          Returns         |
|-------------------------------|--------------------------|
| **`val`:** the object to hash | **`str`:** hashed object |