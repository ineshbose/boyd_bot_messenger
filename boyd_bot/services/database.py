import uuid
from pymongo import MongoClient
from .. import guard


class Database:
    """
    A modular, custom API for the database that will store necessary details about users for fetching their timetable.
    """

    def __init__(self, db_token, key1, key2):
        self.cluster = MongoClient(db_token)
        self.collection = self.cluster[key1]
        self.db = self.collection[key2]

    def sanitize(self, user_data):
        data_to_return = {}
        if user_data:
            for data in user_data:
                data_to_return[data] = (
                    user_data[data]
                    if data not in ["uni_id", "uni_pw"]
                    else guard.decrypt(user_data[data])
                )
        return data_to_return

    def get_data(self, uid):
        user_data = self.db.find_one({"_id": uid})
        return self.sanitize(user_data)

    def delete_data(self, uid):
        return self.db.delete_one({"_id": uid}).deleted_count

    def insert_data(self, uid, **kwargs):
        data_to_add = {"_id": uid}
        for kw in kwargs:
            data_to_add[kw] = (
                kwargs[kw]
                if kw not in ["uni_id", "uni_pw"]
                else guard.encrypt(kwargs[kw])
            )
        return self.db.insert_one(data_to_add)

    def insert_in_reg(self, uid, platform_user):
        reg_id = uuid.uuid4().hex
        while self.get_data(reg_id):
            reg_id = uuid.uuid4().hex
        self.insert_data(uid, reg_id=reg_id, platform_user=platform_user)
        self.insert_data(reg_id, user_id=uid, platform_user=platform_user)
        return reg_id

    def check_registered(self, uid):
        data = self.get_data(uid)
        return False if (not data or "reg_id" in data) else True

    def check_in_reg(self, uid):
        data = self.get_data(uid)
        return False if (not data or "reg_id" not in data) else True

    def get_user_id(self, reg_id):
        return self.get_data(reg_id)["user_id"]

    def get_reg_id(self, uid):
        return self.get_data(uid)["reg_id"]

    def get_reg_id_result(self, reg_id):
        return self.get_data(reg_id)["platform_user"]

    def clear_db(self):
        return self.db.drop()

    def get_list(self):
        d_to_r = []
        for d in self.db.find({}):
            d_to_r.append(self.sanitize(d))
        return d_to_r