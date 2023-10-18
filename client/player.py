import socket

from client.iclient import IClient

MAX_DATA_SIZE = 1024 # bytes
 
class Player(IClient):
    def __init__(self, addr):
        super().__init__()
        self.address = addr
        self.initSocket()

    def initSocket(self, serverHost="127.0.0.1", serverPort=12345):
        self.socket = socket.socket()
        self.socket.connect((serverHost, serverPort))
        self.socket.send("handshake_connect".encode())
        id = self.socket.recv(1024).decode()
        print("Successfully connected, assigned playerid {}".format(id))

    def startListening(self):
        print("->")
        while True:
            i = input()
            if input != '':
                self.socket.send(i.encode())
                data = self.socket.recv(MAX_DATA_SIZE).decode()
                print(data)