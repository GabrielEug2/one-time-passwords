import os.path
# import json
# import hashlib
# from user import User

from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.config import Config 

class CreateUserScreen(Screen):
    pass
    # print("Criando novo usuário")
    # print("Usuario: ", end='')
    # username = input()
    # print("Senha raiz: ", end='')
    # root_password = input()
    # print("Senha local: ", end='')
    # local_password = input()

    # self.user = User(username, root_password, local_password)

    # with open('.user-info', 'w') as f:
    #     json.dump(new_user.__dict__, f, indent=4)

class LoginScreen(Screen):
    pass

class ClientApp(App):
    def build(self):
        Config.set('graphics', 'width', '600') 
        Config.set('graphics', 'height', '600')

        sm = ScreenManager()

        sm.add_widget(CreateUserScreen(name='create_user'))
        sm.add_widget(LoginScreen(name='login'))

        if os.path.exists('.user-info'):
            sm.current = 'login'
        else:
            # È a primeira vez, então vai pra tela de criação de usuário
            sm.current = 'create_user'

        return sm

if __name__ == '__main__':
    ClientApp().run()

# print("Login")
# print("Usuario: ", end='')
# typed_username = input()
# print("Senha local: ", end='')
# typed_local_password = input()

# if typed_username == user['username'] and \
#     hashlib.md5(typed_local_password.encode('utf-8')).hexdigest() == user['local_password']:
    
#     print("Deseja gerar os tokens? [y/n]")
#     answer = 

# else:
#     print("Usuario ou senha errados")