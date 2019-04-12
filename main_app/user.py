import hashlib

class User:
    def __init__(self, username, seed_password, hash_password=True, last_token_used=None):
        self.username = username

        if hash_password:
            self.seed_password = User._hash_function(seed_password)
        else:
            self.seed_password = seed_password

        self.last_token_used = last_token_used

    @staticmethod
    def _hash_function(text):
        return hashlib.md5(text.encode('utf-8')).hexdigest()