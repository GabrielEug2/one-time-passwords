from user import User
import json

class UserPersistence:
    USERS_FILENAME = 'users.json'

    @classmethod
    def load_all(cls):
        try:
            with open(cls.USERS_FILENAME, 'r') as f:
                objects_array = json.load(f)
        except FileNotFoundError:
            objects_array = []

            with open(cls.USERS_FILENAME, 'w') as f:
                f.write('[]')

        users = []

        for obj in objects_array:
            # Nâo é pra fazer o hash aqui pois já foi salvo hasheado no arquivo
            user = User(
                obj['username'],
                obj['local_password'],
                obj['seed_password'],
                hash_passwords=False
            )

            users.append(user)

        return users

    @classmethod
    def create(cls, user):
        users = cls.load_all()
        user_exists = cls.find_by_username(user.username) is not None

        if not user_exists:
            # Persiste o novo usuário
            users.append(user)

            with open(cls.USERS_FILENAME, 'w') as f:
                json.dump([user.__dict__ for user in users], f, indent=4)

            user_created = True
        else:
            # Seria um update, mas nesse caso não queremos fazer isso
            user_created = False
        
        return user_created

    @classmethod
    def find_by_username(cls, username):
        users = cls.load_all()

        for user in users:
            if username == user.username:
                return user

        return None