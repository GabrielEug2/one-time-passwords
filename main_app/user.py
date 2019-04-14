import hashlib
import secrets

class User:
    def __init__(self, username, seed_password, existing_user=False,
                 last_token_used=None, salt=None):
        self.username = username
        self.last_token_used = last_token_used

        if existing_user:
            # Só estamos reconstruindo o mesmo objeto na memória
            self.seed_password = seed_password
            self.salt = salt
        else:
            # Faz o hash da senha e gera o salt
            # See: https://docs.python.org/3/library/secrets.html#module-secrets
            self.seed_password = User._hash_function(seed_password)
            self.salt = secrets.token_hex(16)

    @staticmethod
    def _hash_function(text):
        return hashlib.md5(text.encode('utf-8')).hexdigest()