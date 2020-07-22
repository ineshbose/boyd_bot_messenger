# [`database.py`](https://github.com/ineshbose/boyd_bot_messenger/blob/master/boyd_bot/services/database.py)



## Packages Used

* [pymongo](https://github.com/mongodb/mongo-python-driver)




## `Database`

Simple implementation of a database to enable OOP.
Most functions are one-liners and easily explainable through their names.


### `Database`.**`cluster`**

Initialiser for `MongoClient()`.


### `Database`.**`collection`**

Index specifier for database in the cluster.


### `Database`.**`db`**

Index specifier for collection in the database.


### Note

A good idea to keep user-data as in JSON format with the following keys:

* Registered Users:
    * `_id`: User ID (**Primary Key**)
    * `uni_id`: User's University ID for login (**ENCRYPTED**)
    * `uni_pass`: User's University Password for login (**ENCRYPTED**)

* In-Registration Users:
    * `_id`: User ID (**Candidate Key**)
    * `reg_id`: User's Registration ID (**SHA256 HASHED**, **Candidate Key**)