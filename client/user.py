import hashlib

class User:
    def __init__(self, username, root_password, local_password):
        self.username = username
        self.root_password = hashlib.md5(root_password.encode('utf-8')).hexdigest()
        self.local_password = hashlib.md5(local_password.encode('utf-8')).hexdigest()

    @classmethod
    def from_config_file(cls, filename):
        with open(filename, 'r') as f:
            user_data = json.load(f)

        return cls(user_data['username'], user_data['root_password'], user_data['local_password'])
