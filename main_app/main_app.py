from user import User
from token_auth import TokenAuth

current_user = TokenAuth.require_auth()

print("\n---Aplicação principal---")
print(f"Bem vindo {current_user.username}!")

input("\nDigite Enter para sair")