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
            print("\n-- Criando novo usuário --")
            username = input("Nome de usuario: ")
            local_password = input("Senha local: ")
            seed_password = input("Senha semente: ")
            print()
            
            user = User(username, local_password, seed_password)
            
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

            user = UserPersistence.find_by_username(username)

            if (user is not None) and (user.local_password_matches(local_password)):
                current_user = user
                
                user_authenticated = True
            elif (user is not None) and (not user.local_password_matches(local_password)):
                print("Senha errada")
            else:
                print("Usuario nao encontrado")
                
        return current_user
