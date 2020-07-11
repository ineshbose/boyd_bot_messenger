import timetable

# Imports for Platform
import requests, json
from flask import make_response

# Imports for Database
from pymongo import MongoClient

# Imports for Parser


# Imports for Guard
import hashlib
from cryptography.fernet import Fernet


class Platform:
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
            return data["originalDetectIntentRequest"][
                "payload"]["data"]["sender"]["id"]
        except KeyError:
            return None

    def reply(self, message=None, context=None):
        res = {"fulfillmentMessages": [], "outputContexts": []}
        message = [message] if (isinstance(message, str) or not message) else message

        for m in message:
            res["fulfillmentMessages"].append({"text": {"text": [m]}})

        if context:
            res["outputContexts"].append(context)

        res = json.dumps(res, indent=4)
        r = make_response(res)
        r.headers["Content-Type"] = "application/json"
        return r


class Database:
    def __init__(self, db_token, key1, key2):
        self.cluster = MongoClient(db_token)
        self.db = self.cluster[key1]
        self.collection = self.db[key2]

    def get_data(self, uid):
        return self.collection.find_one({"_id": uid})

    def delete_data(self, uid):
        return self.collection.delete_one({"_id": uid}).deleted_count

    def insert_data(self, uid, uni_id, uni_pw):
        return self.collection.insert_one(
            {"_id": uid, "uni_id": uni_id, "uni_pw": uni_pw}
        )

    def insert_in_reg(self, uid, reg_id):
        return self.collection.insert_one({"_id": uid, "reg_id": reg_id})

    def check_registered(self, uid):
        data = self.get_data(uid)
        return False if (not data or "reg_id" in data) else True

    def check_in_reg(self, uid):
        data = self.get_data(uid)
        return False if (not data or "reg_id" not in data) else True

    def get_user_id(self, reg_id):
        return self.collection.find_one({"reg_id": reg_id})["_id"]

    def get_reg_id(self, uid):
        return self.get_data(uid)["reg_id"]

    def check_reg_data(self, reg_id):
        return True if self.collection.find_one({"reg_id": reg_id}) else False


class Parser:
    def __init__(self):
        pass

    def delete_data(self, uid, db):
        return "Deleted! :)" if db.delete_data(uid) else "Something went wrong. :("

    def read_timetable(self, uid, data):

        param = data["queryResult"]["parameters"]
        dt_param = param["date-time"]
        message = []
        args = []

        if not dt_param:
            args.extend([None, None])
            args.append(param["class-name"])
            message.extend(timetable.read(uid, *args))

        else:

            for single_dt in dt_param:
                args.clear()
                param_keys = {
                    "date_time": ["date_time"],
                    "startDateTime": ["startDateTime", "endDateTime"],
                    "startDate": ["startDate", "endDate"],
                    "startTime": ["startTime", "endTime"],
                }

                for p_key in param_keys:
                    if p_key in single_dt:
                        dt_keys = param_keys[p_key]
                        args.extend(
                            [
                                single_dt[dt_keys[0]],
                                single_dt[dt_keys[1]] if len(dt_keys) > 1 else None,
                            ]
                        )
                        break

                if not args:
                    dt_val = (
                        single_dt[:10] + "T00:00:00" + single_dt[19 : len(single_dt)]
                    )
                    args.extend([dt_val, None])

                args.append(param["class-name"])
                message.extend(timetable.read(uid, *args))

        return message

    def parse(self, request_data, uid, db):

        intent = request_data["queryResult"]["intent"]
        message_text = request_data["queryResult"]["queryText"]
        default_reply = None

        if not intent:
            return default_reply

        intent_name = intent["displayName"].lower().replace(" ", "_")
        intent_linking = {
            "delete_data": lambda: self.delete_data(uid, db),
            "read_timetable": lambda: self.read_timetable(uid, request_data),
        }

        return (
            intent_linking[intent_name]()
            if intent_name in intent_linking
            else default_reply
        )


class Guard:
    def __init__(self, key):
        self.fernet = Fernet(key)

    def encrypt(self, val):
        return self.fernet.encrypt(val.encode())

    def decrypt(self, val):
        return (self.fernet.decrypt(val)).decode()

    def sha256(self, val):
        return hashlib.sha256(val.encode()).hexdigest()

    def sanitized(self, request, key, db=None):
        key = [key] if isinstance(key, str) else key

        for k in key:
            if k not in request:
                return False

        if db:
            uid = request[key[0]]
            return db.check_reg_data(uid) or db.get_data(uid)
