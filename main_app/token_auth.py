from user import User
from persistence.user_persistence import UserPersistence
import token_gen_algorithm as token_gen

class TokenAuth:
    @classmethod
    def require_auth(cls):
        current_user = None

        while current_user is None:
            print("1 - Login")
            print("2 - Novo usuário")
            option = input("Escolha uma opcao: ")

            if option == '1':
                user_authenticating = cls.ask_for_username()
            
                cls.ask_for_token(user_authenticating)

                current_user = user_authenticating
            elif option == '2':
                new_user = cls.ask_for_new_user_info()

                # TODO: mostrar o salt gerado

                cls.ask_for_token(new_user)

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
            seed_password = input("Senha semente: ")
            print()

            user = User(username, seed_password)

            if UserPersistence.create(user):
                user_created = True
            else:
                print("O usuário já existe")

        return user

    @classmethod
    def ask_for_username(cls):
        user_exists = False

        while not user_exists:
            print("\n-- Login --")
            username = input("Usuario: ")

            user = UserPersistence.find_by_username(username)

            if user is not None:
                user_exists = True
            else:
                print("Usuario nao encontrado")

        return user

    @classmethod
    def ask_for_token(cls, user):
        valid_token = False

        while not valid_token:
            token = input("\nToken: ")
            
            if cls.token_is_valid(token, user):
                cls.consume_token(token, user)

                valid_token = True
            else:
                print("Token inválido ou expirado")

    @classmethod
    def token_is_valid(cls, user_token, user):
        N_TOKENS = 5

        valid_tokens_for_user = token_gen.generate_tokens(user.seed_password, N_TOKENS)

        # O último token utilizado e os tokens que podem
        # ser gerados a partir dele não são válidos, então
        # eles são removidos da lista
        if (user.last_token_used is not None) and (user.last_token_used in valid_tokens_for_user):
            last_token_index = valid_tokens_for_user.index(user.last_token_used)

            del valid_tokens_for_user[last_token_index:]

        for token in valid_tokens_for_user:
            if token == user_token:
                return True

        return False

    @classmethod
    def consume_token(cls, token, user):
        user.last_token_used = token

        UserPersistence.update_token_info(user)