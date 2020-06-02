# [facebook.py](https://github.com/ineshbose/boyd_bot_messenger/blob/master/facebook.py)
This script takes advantage of Facebook API to make requests.


## Packages Used
* [requests](https://github.com/psf/requests)


## `send_message()`
```python
def send_message(uid, access_token, message):
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
    
    return requests.post('https://graph.facebook.com/v7.0/me/messages?access_token={}'.format(access_token), json=data)
```



## `verify()`
```python
def verify(uid, access_token):
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
    req = requests.get("https://graph.facebook.com/v7.0/{}?access_token={}".format(uid, access_token))
    return req.json()
```