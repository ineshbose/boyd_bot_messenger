import requests


def send_message(uid, access_token, message):

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
    req = requests.get("https://graph.facebook.com/v7.0/{}?access_token={}".format(uid, access_token))
    return req.json()