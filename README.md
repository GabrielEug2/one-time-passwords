# Geração de senhas descartáveis (One Time Passwords)

É composto de duas partes:

* __Gerador de senhas__: após a autenticação com nome de usuário e senha, permite gerar tokens para utilizar na aplicação principal.

* __Aplicação principal__: consome tokens para realizar a autenticação.

OBS: não há nenhuma forma de comunicação entre as 2 aplicações.