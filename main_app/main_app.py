from token_auth import TokenAuth
from user import User

current_user = TokenAuth.require_auth()

print("\n---Aplicação principal---")
print(f"Bem vindo {current_user.username}!")

input("\nDigite Enter para sair")