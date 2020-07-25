import hashlib
from cryptography.fernet import Fernet


class Guard:
    """
    Features methods for necessary security protocols.
    """

    def __init__(self, key):
        if not key:
            if not os.path.exists(".fernet.key"):
                open(".fernet.key", "wb").write(Fernet.generate_key())
            key = open(".fernet.key", "r").read()
        self.guard = Fernet(key)

    def encrypt(self, val):
        return self.guard.encrypt(val.encode())

    def decrypt(self, val):
        return (self.guard.decrypt(val)).decode()

    def sha256(self, val):
        return hashlib.sha256(val.encode()).hexdigest()

    def sanitized(self, request, key, val=None, db=None):
        result = False
        request = [request] if not isinstance(request, list) else request
        key = [key] if not isinstance(key, list) else key

        for r in request:
            for k in key:
                if k in r:
                    result = True
                    if val:
                        result = True if r[k] == val else False
                    if db:
                        uid = r[k]
                        result = result and (db.check_reg_data(uid) or db.get_data(uid))
                    break

        return result
