import requests, json
from flask import make_response


class Platform:
    """
    Contains methods for interacting with the platform / messaging service.
    """

    def __init__(self, platform_token):
        """
        Initialise class with a token provided by the platform.
        """
        self.platform_token = platform_token

    def send_message(self, uid, message):
        """
        Send message to a platform user through their ID.
        """

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
        """
        Get basic information about the user from the platform.
        """
        req = requests.get(
            "https://graph.facebook.com/v7.0/{}?access_token={}".format(
                uid, self.platform_token
            )
        )
        return req.json()

    def get_id(self, data):
        """
        Get user's ID assigned by the platform.
        """
        try:
            return (
                data["originalDetectIntentRequest"]["payload"]["data"]["sender"]["id"],
                True,
            )
        except (KeyError, TypeError):
            return (
                data["session"].split(":" if ":" in data["session"] else "/")[-1]
                if (data and "session" in data)
                else None,
                False,
            )

    def reply(self, message=None):
        """
        Send a response to a message sent by the user.
        """
        res = {"fulfillmentMessages": []}
        message = [message] if not isinstance(message, list) else message

        for m in message:
            res["fulfillmentMessages"].append({"text": {"text": [m]}})

        res = json.dumps(res, indent=4)
        r = make_response(res)
        r.headers["Content-Type"] = "application/json"
        return r
