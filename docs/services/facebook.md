# WIP

## [Facebook Messenger](https://developers.facebook.com/products/messenger/)

Implemented in _class_ `Platform`.


### `Platform`.**`platform_token`**

Page Access Token for the Facebook Page app.


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