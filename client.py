import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.connect(('localhost', 8686))
for i in range(100):
    sock.send(b'Hello World!')
    print(sock.recv(1024))

