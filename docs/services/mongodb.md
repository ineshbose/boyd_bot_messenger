# WIP

## [mongoDB](https://www.mongodb.com/)

Implemented in _class_ `Database`. This enables mongoDB to be easily replacable (with say `Redis`).
Most functions are one-liners and easily explainable through their names.


### `Database`.**`cluster`**

Initialiser for `MongoClient()`.


### `Database`.**`db`**

Index specifier for database in the cluster.


### `Database`.**`collection`**

Index specifier for collection in the database.


### Note

A good idea to keep user-data as in JSON format with the following keys:

* `_id`: User ID (**Primary Key**)
* `uni_id`: User's University ID for login (**ENCRYPTED**)
* `uni_pass`: User's University Password for login (**ENCRYPTED**)
* `reg_id`: User's Registration ID (**SHA256 HASHED**)