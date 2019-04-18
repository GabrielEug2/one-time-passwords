from password_auth import PasswordAuth
from user import User

import token_gen_algorithm as token_gen
from datetime import datetime
from datetime import timedelta
import time

N_TOKENS = 5

print("\n---Gerador de tokens---")
current_user = PasswordAuth.require_auth()

print("\n---Gerador de tokens---")
print(f"Bem vindo {current_user.username}!")
print(f"Você tem direito a {N_TOKENS} tokens a cada minuto.")
print("  * Se os tokens expirarem, você poderá gerar mais imediatamente.")
print("  * Se utilizar todos, deverá esperar até poder gerar mais.")

while True:
    # Espera até o usuário pedir para gerar
    input("\nAperte Enter para gerar novos tokens.\n")

    last_generation_time = datetime.now()
    tokens = token_gen.generate_tokens(current_user.seed_password, N_TOKENS)

    tokens_expiration_time = last_generation_time.replace(second=0, microsecond=0) + timedelta(minutes=1)

    # Exibe um por um conforme o usuário for solicitando
    print("Tokens gerados. Aperte Enter para visualizar o próximo token")
    
    tokens_expired = False
    for token in tokens:
        print(token, end='')
        input()

        if datetime.now() >= tokens_expiration_time:
            # Não adianta continuar exibindo
            tokens_expired = True
            break

    if tokens_expired:
        print("\nEstes tokens expiraram.")
    else:
        while datetime.now() < tokens_expiration_time:
            time_until_tokens_expiration = tokens_expiration_time - datetime.now()

            print(f"Aguarde {time_until_tokens_expiration // timedelta(seconds=1)}s para gerar mais tokens.", end='\r')

            time.sleep(1)
        print()