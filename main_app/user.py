import hashlib

class User:
    def __init__(self, username, seed_password, last_token_used=None, existing_user=False):
        self.username = username

        if existing_user:
            # Se foi persistido, a senha foi hasheada.
            # Queremos somente reconstruir o mesmo objeto na memória
            self.seed_password = seed_password
        else:
            self.seed_password = User._hash_function(seed_password)

        self.last_token_used = last_token_used

    @staticmethod
    def _hash_function(text):
        return hashlib.md5(text.encode('utf-8')).hexdigest()