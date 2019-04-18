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
            # Antes de salvar a senha, combina com um salt e aplica um hash
            self.salt = User._salt_generator()
            self.seed_password = User._hash_function(seed_password + self.salt)

    @staticmethod
    def _hash_function(text):
        return hashlib.md5(text.encode('utf-8')).hexdigest()

    @staticmethod
    def _salt_generator():
        # O módulo secrets gera números aleatórios criptograficamente seguros
        # 16 bytes = 32 caracteres hex
        return secrets.token_hex(16)