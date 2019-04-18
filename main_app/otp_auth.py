from user import User
from persistence.user_persistence import UserPersistence
import token_gen_algorithm as token_gen

# OTP = One-time Password
class OTPAuth:
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

                print("Quase lá! Para terminar o seu cadastro, abra o gerador " +
                      "de senhas no seu dispositivo, selecione \"Novo usuário\" " +
                      "e insira suas informações.\n")
                print("Quando solicitado, insira o salt abaixo: ")
                print(new_user.salt)

                current_user = cls.ask_for_login_info()
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
            print()

            user = User(username, seed_password)

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
            token = input("Token: ")
            print()

            user = UserPersistence.find_by_username(username)

            if (user is not None) and (cls.token_is_valid(token, user)):
                cls.consume_token(token, user)
                current_user = user
                print("Token aceito")

                user_authenticated = True
            elif user is not None:
                print("Token inválido ou expirado")
            else:
                print("Usuário não encontrado")

        return current_user

    @classmethod
    def token_is_valid(cls, user_token, user):
        N_TOKENS = 5

        valid_tokens_for_user = token_gen.generate_tokens(user.seed_password, N_TOKENS)

        # O último token utilizado e os tokens que podem ser gerados
        # a partir dele não são válidos, então eles são removidos da lista
        if ((user.last_token_used is not None) and
            (user.last_token_used in valid_tokens_for_user)):

            last_token_index = valid_tokens_for_user.index(user.last_token_used)
            # O "+1" é para incluir a posição do token em questão
            del valid_tokens_for_user[:last_token_index+1]

        for token in valid_tokens_for_user:
            if token == user_token:
                return True

        return False

    @classmethod
    def consume_token(cls, token, user):
        user.last_token_used = token

        UserPersistence.update_token_info(user)