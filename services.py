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
    def __init__(self, access_token):
        self.access_token = access_token

    def send_message(self, uid, message):

        data = {
            "messaging_type": "RESPONSE",
            "recipient": {"id": uid},
            "message": {"text": message},
        }

        return requests.post(
            "https://graph.facebook.com/v7.0/me/messages?access_token={}".format(
                self.access_token
            ),
            json=data,
        )

    def get_user_data(self, uid):
        req = requests.get(
            "https://graph.facebook.com/v7.0/{}?access_token={}".format(
                uid, self.access_token
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
    def __init__(self, cluster, db, collection):
        self.cluster = MongoClient(cluster)
        self.db = self.cluster[db]
        self.collection = self.db[collection]

    def find(self, data):
        return self.collection.find_one(data)

    def delete(self, data):
        return self.collection.delete_one(data).deleted_count

    def insert(self, data):
        return self.collection.insert_one(data)

    def exists(self, data):
        return self.collection.count_documents(data)

    def get_data(self, uid):
        return self.find({"_id": uid})

    def insert_data(self, uid, uni_id, uni_pw):
        return self.insert({"_id": uid, "uni_id": uni_id, "uni_pw": uni_pw})

    def delete_data(self, uid):
        return self.delete({"_id": uid})

    def get_user_id(self, reg_id):
        return self.find({"reg_id": reg_id})["_id"]

    def insert_in_reg(self, uid, reg_id):
        return self.insert({"_id": uid, "reg_id": reg_id})

    def delete_in_reg(self, uid, reg_id):
        return self.delete({"_id": uid, "reg_id": reg_id})

    def check_registered(self, uid):
        data = self.find({"_id": uid})
        return False if (not data or "reg_id" in data) else True

    def check_in_reg(self, uid):
        data = self.find({"_id": uid})
        return False if (not data or "reg_id" not in data) else True

    def check_reg_data(self, reg_id):
        return self.exists({"reg_id": reg_id})


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
                param_link = {
                    "date_time": lambda: [single_dt["date_time"], None,],
                    "startDateTime": lambda: [
                        single_dt["startDateTime"],
                        single_dt["endDateTime"],
                    ],
                    "startDate": lambda: [single_dt["startDate"], single_dt["endDate"]],
                    "startTime": lambda: [single_dt["startTime"], single_dt["endTime"]],
                    "default": lambda: [
                        (single_dt[:10] + "T00:00:00" + single_dt[19 : len(single_dt)]),
                        None,
                    ],
                }

                args.extend(
                    param_link.get(next(iter(single_dt)), param_link["default"])()
                )
                args.append(param["class-name"])
                message.extend(timetable.read(uid, *args))

        return message


class Guard:
    def __init__(self, key):
        self.fernet = Fernet(key)

    def encrypt(self, val):
        return self.fernet.encrypt(val.encode())

    def decrypt(self, val):
        return (self.fernet.decrypt(val)).decode()

    def sha256(self, val):
        return hashlib.sha256(val.encode()).hexdigest()
