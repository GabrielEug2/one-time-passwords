from otp_auth import OTPAuth
from user import User

current_user = OTPAuth.require_auth()

print("\n---Aplicação principal---")
print(f"Bem vindo {current_user.username}!")

input("\nDigite Enter para sair")