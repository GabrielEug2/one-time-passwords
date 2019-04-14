from user import User
from persistence.user_persistence import UserPersistence

class PasswordAuth:
    @classmethod
    def require_auth(cls):
        current_user = None

        while current_user is None:
            print("1 - Login")
            print("2 - Novo usuário")
            option = input("Escolha uma opcao: ")

            if option == '1':
                current_user = cls.ask_for_login_info()
            elif option == '2':
                new_user = cls.ask_for_new_user_info()

                # Já faz login direto após o cadastro
                current_user = new_user
            else:
                print("Opcao invalida")
        
        return current_user

    @classmethod
    def ask_for_new_user_info(cls):
        user_created = False

        while not user_created:
            print("\n-- Cadastro --")
            username = input("Nome de usuario: ")
            seed_password = input("Senha semente: ")
            salt = input("Salt (gerado ao se cadastrar na aplicação principal): ")
            local_password = input("Senha local (será usada para acessar o gerador nas próximas vezes): ")
            print()
            
            user = User(username, local_password, seed_password, salt)
            
            if UserPersistence.create(user):
                user_created = True
            else:
                print("O usuário já existe")

        return user

    @classmethod
    def ask_for_login_info(cls):
        user_authenticated = False

        while not user_authenticated:
            print("\n-- Login --")
            username = input("Usuario: ")
            local_password = input("Senha local: ")
            print()

            user = UserPersistence.find_by_username(username)

            if (user is not None) and (user.local_password_matches(local_password)):
                current_user = user
                
                user_authenticated = True
            else:
                print("Usuário ou senha incorretos")
                
        return current_user
