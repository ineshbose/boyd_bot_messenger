# [`database.py`](https://github.com/ineshbose/boyd_bot_messenger/blob/master/boyd_bot/services/database.py)



## Packages Used

* [pymongo](https://github.com/mongodb/mongo-python-driver)



## `Database`

Simple implementation of a database to enable OOP.


### `Database`.**`cluster`**

Initialiser for `MongoClient()`.


### `Database`.**`collection`**

Index specifier for database in the cluster.


### `Database`.**`db`**

Index specifier for collection in the database.


### `Database`.**`get_data(uid)`**

Gets data corresponding to `uid` (primary key - user/sender/registration ID).
The data is broken down into a dictionary to return as an extra step for integrity.

### `Database`.**`delete_data(uid)`**

Deletes data corresponding to `uid` (primary key).

### `Database`.**`insert_data(uid, uni_id=None, uni_pw=None):

Inserts data into database for a registered user. If credentials are not supposed to be remembered, only user/sender ID is stored.

### `Database`.**`insert_in_reg(uid)`**

Hashes `uid` and inserts registration data accordingly. Inserts two sets due to the primary key relation.


### Note

A good idea to keep user-data as in JSON format with the following keys:

* Registered Users:
    * `_id`: User ID (**Primary Key**)
    * `uni_id`: User's University ID for login (**ENCRYPTED**)
    * `uni_pass`: User's University Password for login (**ENCRYPTED**)

* In-Registration Users:
    * `_id`: User ID (**Candidate Key**)
    * `reg_id`: User's Registration ID (**Candidate Key**)