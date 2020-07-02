import requests, timetable, json
from pymongo import MongoClient
from flask import make_response


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


class Database:
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
        return self.delete(self.wait_id + uid)

    def insert_waiting(self, uid):
        return self.insert({"_id": self.wait_id + uid})

    def exists_waiting(self, uid):
        return self.exists(self.wait_id + uid)

    def insert_data(self, uid, uni_id, uni_pw):
        return self.insert({"_id": uid, "uni_id": uni_id, "uni_pw": uni_pw})


class Parser:
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

    def read_timetable(self, uid, data):

        param = data["queryResult"]["parameters"]
        args = []
        dtparam = next(iter(param["date-time"]), None)

        if not dtparam:
            args.extend([None, None])

        else:

            param_link = {
                "date_time": lambda: [dtparam["date_time"], None,],
                "startDateTime": lambda: [
                    dtparam["startDateTime"],
                    dtparam["endDateTime"],
                ],
                "startDate": lambda: [dtparam["startDate"], dtparam["endDate"]],
                "startTime": lambda: [dtparam["startTime"], dtparam["endTime"]],
                "default": lambda: [
                    (dtparam[:10] + "T00:00:00" + dtparam[19 : len(dtparam)]),
                    None,
                ],
            }

            args.extend(param_link.get(next(iter(dtparam)), param_link["default"])())

        args.append(next(iter(param["class-name"]), None))

        return timetable.read(uid, *args)

    def prepare_json(self, message=None, context=None):
        res = {"fulfillmentMessages": [], "outputContexts": []}

        if isinstance(message, list):
            for m in message:
                res["fulfillmentMessages"].append({"text": {"text": [m]}})
        else:
            res["fulfillmentMessages"].append({"text": {"text": [message]}})

        if context:
            res["outputContexts"].append(context)

        res = json.dumps(res, indent=4)
        r = make_response(res)
        r.headers["Content-Type"] = "application/json"
        return r
