# [`guard.py`](https://github.com/ineshbose/boyd_bot_messenger/blob/master/boyd_bot/services/guard.py)



## Packages Used

* [cryptography](https://github.com/pyca/cryptography)




## `Guard`

Contains methods essential for security.


### `Guard`.**`fernet`**

Initialiser for `Fernet()`.


### `Guard`.**`encrypt(val)`**

Encodes and encrypts `val` according to Fernet key.

|            Parameters            |             Returns            |
|----------------------------------|--------------------------------|
| **`val`:** the object to encrypt | **`binary`:** encrypted object |


### `Guard`.**`decrypt(val)`**

Decrypts and decodes `val` according to Fernet key.

|            Parameters            |           Returns           |
|----------------------------------|-----------------------------|
| **`val`:** the object to decrypt | **`str`:** decrypted object |


### `Guard`.**`sha256(val)`**

Hashes `val` using SHA-256 algorithm with `hashlib`.

|          Parameters           |          Returns         |
|-------------------------------|--------------------------|
| **`val`:** the object to hash | **`str`:** hashed object |


### `Guard`.**`sanitized(request, key, val=None, db=None)`**

Verifies if a request is safe/sanitized.

|                                                                                           Parameters                                                                                          |          Returns         |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------|
| **`request`:** the request made as a JSON<br>**`key`:** the element the request MUST have<br>**`val`:** the required corresponding value<br>**`db`:** instance of `Database` for more verification | **`bool`:** if sanitized |