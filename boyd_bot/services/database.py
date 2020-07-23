from pymongo import MongoClient
from .. import guard


class Database:
    def __init__(self, db_token, key1, key2):
        self.cluster = MongoClient(db_token)
        self.collection = self.cluster[key1]
        self.db = self.collection[key2]

    def get_data(self, uid):
        user_data = self.db.find_one({"_id": uid})
        data_to_return = {}
        if user_data:
            for data in user_data:
                data_to_return[data] = (
                    user_data[data]
                    if data not in ["uni_id", "uni_pw"]
                    else guard.decrypt(user_data[data])
                )
        return data_to_return

    def delete_data(self, uid):
        return self.db.delete_one({"_id": uid}).deleted_count

    def insert_data(self, uid, uni_id=None, uni_pw=None):
        data_to_add = (
            {"_id": uid}
            if not (uni_id and uni_pw)
            else {
                "_id": uid,
                "uni_id": guard.encrypt(uni_id),
                "uni_pw": guard.encrypt(uni_pw),
            }
        )
        return self.db.insert_one(data_to_add)

    def insert_in_reg(self, uid):
        hash_id = guard.sha256(uid)
        reg_id = hash_id[:15] if not self.check_reg_data(hash_id[:15]) else hash_id
        self.db.insert_one({"_id": uid, "reg_id": reg_id})
        self.db.insert_one({"_id": reg_id, "user_id": uid})
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

    def check_reg_data(self, reg_id):
        return True if self.get_data(reg_id) else False
