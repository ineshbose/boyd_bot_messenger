import os
import hashlib
from cryptography.fernet import Fernet


class Guard:
    """
    Features methods for necessary security protocols.
    """

    def __init__(self, key):
        """
        Creating an instance of the encryption package.
        """
        if not key:  # Generate own key if no key is provided
            if not os.path.exists(".fernet.key"):
                open(".fernet.key", "wb").write(Fernet.generate_key())
            key = open(".fernet.key", "r").read()
        self.guard = Fernet(key)

    def encrypt(self, val):
        """
        Encrypt a passed value using the key.
        """
        return self.guard.encrypt(val.encode())

    def decrypt(self, val):
        """
        Decrypt a passed value through the key.
        """
        return (self.guard.decrypt(val)).decode()

    def sha256(self, val):
        """
        Provide a SHA256 hash of a passed value.
        """
        return hashlib.sha256(val.encode()).hexdigest()

    def sanitized(self, request, key, val=None):
        """
        Check for keys and values in a dictionary/request.
        """
        result = False
        key = [key] if not isinstance(key, list) else key
        if all(k in request for k in key):
            result = True
            if val:
                result = val in request.values()

        return result
