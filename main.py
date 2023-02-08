import socket


client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.connect(('10.171.132.94', 2500))
time = client_sock.recv(1024).decode()
print(time)
client_sock.close()
