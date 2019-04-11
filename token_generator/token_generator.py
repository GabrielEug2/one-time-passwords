from user import User
from persistence.user_persistence import UserPersistence

import token_gen_algorithm as token_gen
from datetime import datetime
from datetime import timedelta
import time

def create_new_user():
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

def login():
    user_authenticated = False

    while not user_authenticated:
        print("\n-- Login --")
        username = input("Usuario: ")
        local_password = input("Senha local: ")
        
        user = UserPersistence.find_by_username(username)

        if (user is not None) and (user.local_password_matches(local_password)):
            user_authenticated = True
            current_user = user
        elif (user is not None) and (not user.local_password_matches(local_password)):
            print("Senha errada")
        else:
            print("Usuario nao encontrado")
    
    return current_user


if __name__ == '__main__':
    print("1 - Login")
    print("2 - Novo usuário")
    option = input("Escolha uma opcao: ")

    if option == '1':
        current_user = login()
    elif option == '2':
        current_user = create_new_user()
    else:
        print("Opcao invalida")
        exit()

    # A partir desse momento está logado como current_user

    n_tokens = 5
    print("\n---Gerador de tokens---")
    print(f"Bem vindo {current_user.username}!")
    print(f"Você pode gerar {n_tokens} tokens a cada minuto. Se " +
            "usar todos, deverá aguardar até o próximo minuto.")

    while True:
        # Espera até o usuário pedir para gerar os tokens
        input("\nAperte Enter quando quiser gerar os tokens.\n")

        time_of_last_generation = datetime.now()
        tokens = token_gen.generate_tokens(current_user.seed_password, n_tokens)

        # Antes de exibir:
        #   * Inverte a ordem, porque a partir de um token é
        #     possível regerar os próximos (e obviamente não
        #     queremos isso)
        #   * Deixa só os N primeiros caracteres de cada token,
        #     porque seria chato ter que digitar um token grande
        tokens.reverse()

        tokens = [token[0:6] for token in tokens]

        # Exibe um por um conforme o usuário solicita
        print("Tokens gerados. Aperte Enter para visualizar o próximo token")
        
        for token in tokens:
            print(token, end='')
            input()

        print("\nAguarde o próximo minuto para gerar mais tokens.")

        next_tokens_unlock_time = time_of_last_generation.replace(second=0, microsecond=0) + timedelta(minutes=1)

        while datetime.now() < next_tokens_unlock_time:
            print("...")

            time.sleep(5)

