import json
import requests
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
        self.msg_char_limit = 2000

    def sanitize_messages(self, message):
        """
        Keeps message in a uniform, acceptable way.
        """
        paragraphs = (
            message.split('\n\n')
            if isinstance(message, str) else message
        )

        new_message = []
        temp_group = ""

        for i,paragraph in enumerate(paragraphs):
            temp_group=f"{temp_group}{paragraph}\n\n"

            if i == len(paragraphs) - 1:
                new_message.append(temp_group[:-2])
                break

            if len(temp_group + paragraphs[i+1]) >= self.msg_char_limit:
                new_message.append(temp_group[:-2])
                temp_group = ""

        return new_message

    def send_message(self, uid, message):
        """
        Send message to a platform user through their ID.
        """
        return [
            requests.post(
                "https://graph.facebook.com/v7.0/me/messages",
                params={"access_token": self.platform_token},
                json={
                    "recipient": {"id": uid},
                    "message": {"text": m},
                    "messaging_type": "MESSAGE_TAG",
                    "tag": "ACCOUNT_UPDATE"
                }
            ) for m in self.sanitize_messages(message)
        ]

    def get_user_data(self, uid):
        """
        Get basic information about the user from the platform.
        """
        return requests.get(
            f"https://graph.facebook.com/v7.0/{uid}",
            params={"access_token": self.platform_token}
        ).json()

    def get_id(self, data):
        """
        Get user's ID assigned by the platform.
        """
        try:
            return (
                data["originalDetectIntentRequest"][
                    "payload"]["data"]["sender"]["id"],
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
        message = self.sanitize_messages(message) if message else []
        res["fulfillmentMessages"].extend({"text": {"text": [m]}} for m in message)
        res["fulfillmentText"] = "\n".join(message)
        res = json.dumps(res, indent=4)
        r = make_response(res)
        r.headers["Content-Type"] = "application/json"
        return r
