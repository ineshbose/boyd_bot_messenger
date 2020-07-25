# Security

The app deals with users' university credentials and in no way must these be taken lightly. All steps possible should be taken to keep these secure.


## Authentication

```
Never trust user input.
```

Requests received are verified using authentication elements like headers or arguments that contain certain keys. The very first step the app takes if verifying that the data is authentic.

```python
if not guard.sanitized([request.headers, request.args], wb_arg_name, webhook_token):
    return redirect("/", code=403)
```


## Encryption

```
Passwords should NEVER be stored as plain-text.
```

This principle is strict and popular in cyber-security. Along with password, the University ID is also encrypted to add an extra layer of security and anonymity. We, the developers, do not have a say in how a user wants to store their data, therefore it's a responsibility to give them the most options, and safe options. Encrypted University ID is preferred over plain-text ID (even though University IDs aren't usually kept secret - you find them in emails, project sheets, etc). These elements are also required for retrieving calendars, so they need to be decrypted as well and hence are not hashed. **The encryption key must be safe at all costs.**

```python
def encrypt(self, val):
    return self.guard.encrypt(val.encode())

def decrypt(self, val):
    return (self.guard.decrypt(val)).decode()
```


## Anonymity

```
Going through a database, one should face difficulty in finding a specific user's set.
```

There's a tendency to target individuals and if any of their information known, it could get easier to retrieve data by some means (not that it would be easy in the first place). Therefore, University ID should not be stored as plain-text. Another unique and essential information about the user is their platform/sender ID. Even though platforms also provide security for this (for example Facebook provides unique sender ID according to app only), that does not end a developer's responsibility. So a good idea is to hide the sender ID as well.

```python
reg_id = uuid.uuid4().hex
while self.check_reg_data(reg_id):
    reg_id = uuid.uuid4().hex
```


## Variables & Keys

```
If you put a key under the mat for the cops, a burglar can find it, too.
```

Another area is using variables & keys in the app. These keys, for obvious reasons, cannot be shown to the public. Many hosting services like Heroku, PythonAnywhere offer security for these variables/keys. Still! That doesn't end a developer's responsibility. These keys should not be simple, small words like `database_key_boyd` but rather a long, randomised string with absolutely no meaning. Also consider changing them once a while.

```python
key = os.environ["KEY_NAME"]
```


## Note

I just want to make it clear that I'm not an expert on cyber security and doing the best I can out of my knowledge and skills. In this time of the internet, it's pretty difficult to guarantee security, but it's still a responsibility to do your best.