import sys, selectors, socket, hashlib, time


if __name__ == "__main__":
    sel = selectors.DefaultSelector()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(sys.argv[1],int(sys.argv[2]))
    server_socket.listen()
    sel.register(server_socket, selectors.EVENT_READ, data=None)
    users = {}
    def accept(sock):
        client_socket, client_addr = sock.accept()
        sel.register(client_socket, selectors.EVENT_READ, data=auth)

    def auth(sock):
        data = sock.recv(1024)
        if data:
            nickname, password = data.decode().split(':')
            if nickname in users:
                if hashlib.sha1(password.encode()).hexdigest() != users[nickname][1]:
                    sock.sendall('Invalid password'.encode())
                    sel.unregister(sock)
                    sock.close()
                    return
            else:
                sock.sendall('Registering new user'.encode())
                password1 = sock.recv(1024).decode()
                password2 = sock.recv(1024).decode()
                if password1 != password2:
                    sock.sendall('Passwords do not match'.encode())
                    sel.unregister(sock)
                    sock.close()
                    return
            users[nickname] = (nickname, hashlib.sha1(password1.encode()).hexdigest(), sock)
            sel.modify(sock, selectors.EVENT_READ, data=recv_wrapper)
            sock.sendall('Authentication successful'.encode())
        else:
            sel.unregister(sock)
            sock.close()
    def recv_wrapper(sock):
        data = sock.recv(1024)
        if data:
            message = data.decode()
            nickname = users[sock.getpeername()[1]][0]
            timestamp = time.strftime('%H:%M', time.localtime())
            print('{} ({})'.format(nickname, timestamp), message)
            for client in users.values():
                if client[2] != sock:
                    client[2].sendall('{} ({}): {}'.format(nickname, timestamp, message).encode())
        else:
            sel.unregister(sock)
            sock.close()

    while True:
        events = sel.select()
        for key, mask in events:
            callback = key.data
            callback(key.fileobj)
