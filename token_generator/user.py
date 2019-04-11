import hashlib
import json

class User:
    def __init__(self, username, local_password, seed_password, hash_passwords=True):
        self.username = username

        if hash_passwords:
            self.local_password = User._hash(local_password)
            self.seed_password = User._hash(seed_password)
        else:
            self.local_password = local_password
            self.seed_password = seed_password

    def local_password_matches(self, password):
        return self._hash(password) == self.local_password
   
    @staticmethod
    def _hash(text):
        return hashlib.md5(text.encode('utf-8')).hexdigest()