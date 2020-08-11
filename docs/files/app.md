# [`app.py`](https://github.com/ineshbose/boyd_bot_messenger/blob/master/boyd_bot/app.py)

This script has essential implementations that helps the bot function.



## `webhook()`

Enables webhook with the platform/service (like Dialogflow or Facebook Messenger). The request data is fetched (in JSON) and used by other functions. The `GET` method does not have any use but rather redirects users that navigate to `url+"/webhook"`.

```python
>>> import requests
>>> requests.post(app_url+"webhook/", headers={wb_arg_name: webhook_token})
<Response [200]>

>>> requests.get(app_url+"webhook/").url
%APP_URL%
```

|   Returns   |
|-------------|
| **`dict`**  |



## `new_user_registration()`

Registers users to the application by verifying login credentials and adding them in the database. In-registration users are distinguished using a `reg_id` attribute in their data.

```python
>>> import requests
>>> requests.post(app_url+"/register/123", 
                  data={"uni_id": "random_id", "uni_pw": "random_pass"}).url
%APP_URL%
```

|   Returns   |
|-------------|
| **`None`**  |



## `user_gateway(request_data, uid)`

Acts as a gateway for all messages before understanding intents and user attributes by enabling login-integrity and fetching data from the database.

```python
>>> user_gateway({"queryText": "hi there"}, "1234567890")
APP: 1234567890 logging in again.
Hey there!
```

|                                       Parameters                                               |                                  Returns                                 |
|------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------|
| **`request_data`:** the POST request dictionary<br>**`uid`:** the unique sender ID of the user | **`str`:** the response<br>**`None`:** if response is not handled by app |