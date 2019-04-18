import hashlib

class User:
    def __init__(self, username, local_password, seed_password, salt, existing_user=False):
        self.username = username
        self.salt = salt

        if existing_user:
            # Só estamos reconstruindo o mesmo objeto na memória
            self.local_password = local_password
            self.seed_password = seed_password
        else:
            # Antes de salvar as senhas, combina com o salt e aplica um hash
            self.local_password = User._hash_function(local_password + self.salt)
            self.seed_password = User._hash_function(seed_password + self.salt)

    def local_password_matches(self, password):
        return self._hash_function(password + self.salt) == self.local_password
   
    @staticmethod
    def _hash_function(text):
        return hashlib.md5(text.encode('utf-8')).hexdigest()