import pickle
import socket


class Network:
    def __init__(self, ip):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = ip
        self.port = 8686
        self.addr = (self.server, self.port)

    def connect(self):
        try:
            self.client.connect(self.addr)
            a = pickle.loads(self.client.recv(2**16))
            return a # map
        except Exception as e:
            print(e)

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            print(e)

