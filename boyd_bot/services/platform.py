import requests, json
from flask import make_response


class Platform:
    """
    Contains methods for interacting with the platform / messaging service.
    """

    def __init__(self, platform_token):
        self.platform_token = platform_token

    def send_message(self, uid, message):

        data = {
            "messaging_type": "RESPONSE",
            "recipient": {"id": uid},
            "message": {"text": message},
        }

        return requests.post(
            "https://graph.facebook.com/v7.0/me/messages?access_token={}".format(
                self.platform_token
            ),
            json=data,
        )

    def get_user_data(self, uid):
        req = requests.get(
            "https://graph.facebook.com/v7.0/{}?access_token={}".format(
                uid, self.platform_token
            )
        )
        return req.json()

    def get_id(self, data):
        try:
            return data["originalDetectIntentRequest"]["payload"]["data"]["sender"][
                "id"
            ]
        except KeyError:
            return "demo"

    def reply(self, message=None):
        res = {"fulfillmentMessages": []}
        message = [message] if not isinstance(message, list) else message

        for m in message:
            res["fulfillmentMessages"].append({"text": {"text": [m]}})

        res = json.dumps(res, indent=4)
        r = make_response(res)
        r.headers["Content-Type"] = "application/json"
        return r
