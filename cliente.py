import socket, struct, json, threading

# ---------------------------------------------
# Função que monta mensagens no formato do protocolo
# ---------------------------------------------
def montar_msg(cmd, dados):
    payload = json.dumps(dados).encode()
    header = struct.pack('!BBH', cmd, 1, len(payload))
    return header + payload

# ---------------------------------------------
# Thread que fica recebendo mensagens do servidor
# (roda em paralelo ao input do usuário)
# ---------------------------------------------
def receber(sock):
    def recv_all(n):
        data = b''
        while len(data) < n:
            parte = sock.recv(n - len(data))
            if not parte:
                return None
            data += parte
        return data

    while True:
        cab = recv_all(4)
        if not cab:
            break
        cmd, ver, tam = struct.unpack('!BBH', cab)
        payload = recv_all(tam)
        if not payload:
            break
        dados = json.loads(payload.decode())
        print(f"\n[CMD={cmd}] {json.dumps(dados, indent=2)}")

# ---------------------------------------------
# Código principal do cliente
# ---------------------------------------------
sock = socket.socket()
sock.connect(('127.0.0.1', 50000))  # conecta ao servidor local

# inicia a thread que fica ouvindo o servidor
threading.Thread(target=receber, args=(sock,), daemon=True).start()

# envia login e histórico
nome = input("Digite seu nome: ")
sock.sendall(montar_msg(1, {"username": nome}))  # LOGIN
sock.sendall(montar_msg(3, {}))                  # GET_HISTORY

# loop principal de envio de mensagens
while True:
    msg = input("> ")
    if msg.lower() == "sair":
        sock.sendall(montar_msg(4, {}))  # LOGOUT
        break
    sock.sendall(montar_msg(2, {"message": msg}))  # POST_MESSAGE

sock.close()
