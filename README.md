🚀 Como executar
1️⃣ Clonar o repositório
git clone https://github.com/SEU_USUARIO/mural-compartilhado.git
cd mural-compartilhado

2️⃣ Iniciar o servidor

Abra um terminal e execute:

python servidor.py


O servidor escuta na porta 50000 (localhost) por padrão.

Você deve ver algo como:

Servidor iniciado na porta 50000
Aguardando conexões...

3️⃣ Iniciar os clientes

Abra outros terminais e execute:

python cliente.py


Ao iniciar, o cliente pedirá um nome de usuário:

Digite seu nome de usuário:


Digite algo como artur, joao, maria, etc.

4️⃣ Testando o funcionamento

Após conectar:

O servidor responde com "Login realizado com sucesso!"

Você pode digitar mensagens — elas serão enviadas para o mural.

Todos os clientes conectados receberão o broadcast com o novo recado.
