import socket, threading, json, struct, datetime

PORT = 50000  # porta padrão do protocolo
clientes = {}  # dicionário: nome -> socket do cliente
mensagens = []  # lista com o histórico de recados

# ---------------------------------------------
# Função que monta uma mensagem no formato do protocolo:
# [COMANDO][VERSAO][TAMANHO_PAYLOAD][JSON]
# ---------------------------------------------
def montar_msg(cmd, dados):
    payload = json.dumps(dados).encode()           # converte o dicionário em JSON e depois em bytes
    header = struct.pack('!BBH', cmd, 1, len(payload))  # ! = big endian, BBH = 1+1+2 bytes
    return header + payload                        # retorna o cabeçalho + corpo (payload)

# ---------------------------------------------
# Envia uma mensagem para todos os clientes conectados
# (usado no broadcast de novos recados)
# ---------------------------------------------
def enviar_todos(cmd, dados):
    msg = montar_msg(cmd, dados)
    for c in list(clientes.values()):
        try:
            c.sendall(msg)
        except:
            pass  # se der erro, ignora (cliente desconectado)

# ---------------------------------------------
# Função que trata cada cliente em uma thread separada
# ---------------------------------------------
def tratar_cliente(sock):
    nome = None
    while True:
        try:
            cabecalho = sock.recv(4)  # lê os 4 bytes do cabeçalho
            if not cabecalho:
                break
            cmd, ver, tam = struct.unpack('!BBH', cabecalho)  # desempacota: comando, versão, tamanho
            dados = json.loads(sock.recv(tam).decode())  # lê o payload (JSON) e converte para dict
        except:
            break

        # -----------------------------------------
        # 1 - LOGIN
        # -----------------------------------------
        if cmd == 1:
            nome = dados["username"]
            if nome in clientes:
                sock.sendall(montar_msg(200, {"message": "Nome já usado"}))
                break
            clientes[nome] = sock
            sock.sendall(montar_msg(101, {"message": "Login realizado com sucesso!"}))

        # -----------------------------------------
        # 3 - GET_HISTORY
        # -----------------------------------------
        elif cmd == 3:
            sock.sendall(montar_msg(103, {"messages": mensagens}))

        # -----------------------------------------
        # 2 - POST_MESSAGE
        # -----------------------------------------
        elif cmd == 2:
            recado = {
                "author": nome,
                "message": dados["message"],
                "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
            }
            mensagens.append(recado)
            enviar_todos(102, recado)  # envia para todos os clientes

        # -----------------------------------------
        # 4 - LOGOUT
        # -----------------------------------------
        elif cmd == 4:
            break

    # Saiu do loop: remove o cliente e fecha o socket
    if nome in clientes:
        del clientes[nome]
    sock.close()

# ---------------------------------------------
# Código principal do servidor
# ---------------------------------------------
s = socket.socket()
s.bind(('', PORT))
s.listen()
print("Servidor ouvindo na porta", PORT)

while True:
    conn, addr = s.accept()
    # Cria uma thread para cada cliente conectado
    threading.Thread(target=tratar_cliente, args=(conn,), daemon=True).start()
