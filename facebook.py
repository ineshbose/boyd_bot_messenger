import requests


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
    bool
        If user exists (True) or not (False)
    """
    req = requests.get("https://graph.facebook.com/v7.0/{}?access_token={}".format(uid, access_token))
    return False if 'error' in req.json() else True