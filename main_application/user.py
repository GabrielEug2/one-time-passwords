import hashlib
import json

class User:
    USERS_FILENAME = 'users.json'

    def __init__(self, username, local_password, seed_password, hash_passwords=True):
        self.username = username

        if hash_passwords:
            self.local_password = User._hash(local_password)
            self.seed_password = User._hash(seed_password)
        else:
            self.local_password = local_password
            self.seed_password = seed_password

    def save(self):
        users = User.load_all()

        user_exists = User.find_by_username(self.username, users) is not None

        if not user_exists:
            users.append(self)

            with open(User.USERS_FILENAME, 'w') as f:
                json.dump([user.__dict__ for user in users], f, indent=4)

            return True
        else:
            return False

    def local_password_matches(self, password):
        return self._hash(password) == self.local_password

    @classmethod
    def find_by_username(cls, username, users):
        for user in users:
            if username == user.username:
                return user

        return None

    @classmethod
    def load_all(cls):
        users = []

        try:
            with open(User.USERS_FILENAME, 'r') as f:
                users_array = json.load(f)
        except FileNotFoundError:
            with open(User.USERS_FILENAME, 'w') as f:
                f.write('[]')

            users_array = []

        for u in users_array:
            # Nâo é pra fazer o hash aqui pois já foi salvo hasheado no arquivo
            user = User(
                u['username'],
                u['local_password'],
                u['seed_password'],
                hash_passwords=False
            )

            users.append(user)

        return users

    @staticmethod
    def _hash(text):
        return hashlib.md5(text.encode('utf-8')).hexdigest()