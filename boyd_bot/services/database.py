import uuid
from pymongo import MongoClient
from .. import guard


class Database:
    """
    A modular, custom API for the database that will store
    necessary details about users for fetching their timetable.
    """

    def __init__(self, db_token, key1, key2):
        """
        Creating an instance of the database package.
        """
        self.cluster = MongoClient(db_token)
        self.collection = self.cluster[key1]
        self.db = self.collection[key2]
        self.clean_db()  # This clears the database from all one-time-users

    def sanitize(self, user_data):
        """
        Creates a dictionary out of the data.
        """
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
        """
        Fetch data using primary key and return it as a clean dictionary.
        """
        user_data = self.db.find_one({"_id": uid})
        return self.sanitize(user_data)

    def get_all(self):
        """
        Get all data from the database in order to iterate over it.
        """
        return [self.sanitize(d) for d in self.db.find({})]

    def delete_data(self, uid):
        """
        Delete data from the database using primary key and return result.
        """
        return self.db.delete_one({"_id": uid}).deleted_count

    def insert_data(self, uid, **kwargs):
        """
        Insert data into the database with essential attributes.
        """
        data_to_add = {"_id": uid}
        for kw in kwargs:
            data_to_add[kw] = (
                kwargs[kw]
                if kw not in ["uni_id", "uni_pw"]
                else guard.encrypt(kwargs[kw])
            ) if not isinstance(kwargs[kw], bool) else int(kwargs[kw])
        return self.db.insert_one(data_to_add)

    def insert_in_reg(self, uid, platform_user):
        """
        Insert registration data for a user.
        """
        reg_id = uuid.uuid4().hex[:12]
        while self.get_data(reg_id):
            reg_id = uuid.uuid4().hex[:12]
        self.insert_data(uid, reg_id=reg_id, platform_user=platform_user)
        self.insert_data(reg_id, user_id=uid, platform_user=platform_user)
        return reg_id

    def check_registered(self, uid):
        """
        Check if a user is registered with the app.
        """
        data = self.get_data(uid)
        return False if (not data or "reg_id" in data) else True

    def check_in_reg(self, uid):
        """
        Check if a user is in the process of registration.
        """
        data = self.get_data(uid)
        return False if (not data or "reg_id" not in data) else True

    def clean_db(self):
        """
        Check and delete all one-time-user datasets.
        """
        for d in self.get_all():
            if not (d.get("uni_id") or d.get("platform_user")):
                self.delete_data(d["_id"])

    def clear_db(self):
        """
        Remove all data from the database.
        """
        return self.db.drop()
