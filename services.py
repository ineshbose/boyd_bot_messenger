import requests, timetable
from pymongo import MongoClient


class Facebook:
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


class Mongo:
    def __init__(self, cluster, db, collection, wait_id):
        self.cluster = MongoClient(cluster)
        self.db = self.cluster[db]
        self.collection = self.db[collection]
        self.wait_id = wait_id

    def find(self, uid):
        return self.collection.find_one({"_id": uid})

    def delete(self, uid):
        return self.collection.delete_one({"_id": uid}).deleted_count

    def insert(self, data):
        return self.collection.insert_one(data)

    def exists(self, uid):
        return self.collection.count_documents({"_id": uid})

    def delete_waiting(self, uid):
        return self.collection.delete_one({"_id": self.wait_id + uid}).deleted_count

    def insert_waiting(self, uid):
        return self.collection.insert_one({"_id": self.wait_id + uid})

    def exists_waiting(self, uid):
        return self.collection.count_documents({"_id": self.wait_id + uid})


class Dialogflow:
    def __init__(self):
        pass

    def get_id(self, data):
        try:
            return data["originalDetectIntentRequest"][
                "payload"]["data"]["sender"]["id"]
        except KeyError:
            return None

    def delete_data(self, uid, db):
        return "Deleted! :)" if db.delete(uid) else "Something went wrong. :("

    def read_next(self, uid):
        return timetable.read(uid)

    def read_timetable(self, uid, data):
        param = data["queryResult"]["parameters"]["date-time"]

        param_link = {
            "date_time": lambda: (param["date_time"],),
            "startDateTime": lambda: (param["startDateTime"], param["endDateTime"]),
            "startDate": lambda: (param["startDate"], param["endDate"]),
            "startTime": lambda: (param["startTime"], param["endTime"]),
            "default": lambda: ((param[:10] + "T00:00:00" + param[19 : len(param)]),),
        }

        return timetable.read(
            uid, *(param_link.get(next(iter(param)), param_link["default"])())
        )
