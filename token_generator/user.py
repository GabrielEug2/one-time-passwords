import hashlib

class User:
    def __init__(self, username, local_password, seed_password, existing_user=False):
        self.username = username

        if existing_user:
            # Se foi persistido, as senhas foram hasheadas.
            # Queremos somente reconstruir o mesmo objeto na memória
            self.local_password = local_password
            self.seed_password = seed_password
        else:
            self.local_password = User._hash_function(local_password)
            self.seed_password = User._hash_function(seed_password)

    def local_password_matches(self, password):
        return self._hash_function(password) == self.local_password
   
    @staticmethod
    def _hash_function(text):
        return hashlib.md5(text.encode('utf-8')).hexdigest()