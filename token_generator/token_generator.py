from password_auth import PasswordAuth
from user import User

import token_gen_algorithm as token_gen
from datetime import datetime
from datetime import timedelta
import time

N_TOKENS = 5

current_user = PasswordAuth.require_auth()

print("\n---Gerador de tokens---")
print(f"Bem vindo {current_user.username}!")
print(f"Você pode gerar {N_TOKENS} tokens a cada minuto. Se " +
        "usar todos, deverá aguardar até o próximo minuto.")

while True:
    # Espera até o usuário pedir para gerar os tokens
    input("\nAperte Enter quando quiser gerar os tokens.\n")

    time_of_last_generation = datetime.now()
    tokens = token_gen.generate_tokens(current_user.seed_password, current_user.salt, N_TOKENS)

    # Exibe um por um conforme o usuário solicita
    print("Tokens gerados. Aperte Enter para visualizar o próximo token")
    
    for token in tokens:
        print(token, end='')
        input()

    # Espera até poder gerar mais
    print("\nAguarde o próximo minuto para gerar mais tokens.")

    next_tokens_unlock_time = time_of_last_generation.replace(second=0, microsecond=0) + timedelta(minutes=1)

    while datetime.now() < next_tokens_unlock_time:
        print("...")

        time.sleep(5)