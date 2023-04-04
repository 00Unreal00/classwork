import sys, socket, selectors
if __name__ == "__main__":
    sel = selectors.DefaultSelector()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    HOST = sys.argv[1]
    PORT = int(sys.argv[2])
    s.connect((HOST, PORT))
    s.setblocking(False)
    def read(soc):
        data = soc.recv(10000)
        print(data.decode().strip("\n"))

    def send(d):
        data = d.readline()
        s.sendall(data.encode())
    sel.register(sys.stdin, selectors.EVENT_READ, send)
    sel.register(s, selectors.EVENT_READ, read)

    while True:
        events = sel.select()
        for key, mask in events:
            key.data(key.fileobj)