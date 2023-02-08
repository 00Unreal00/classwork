import socket
from datetime import datetime


serv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto=0)
serv_sock.bind(('10.171.132.94', 2500))
serv_sock.listen(10)
while True:
    client_sock, client_addr = serv_sock.accept()
    print('Nikita Ermakov:', datetime.now())
    while True:
        data = client_sock.recv(1024)
        if not data:
            break
        client_sock.sendall(data)

client_sock.close()