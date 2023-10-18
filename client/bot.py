import socket

from client.iclient import IClient

MAX_DATA_SIZE = 1024

class Bot(IClient):
    def __init__(self):
        super().__init__()
        self.playerId = None
        self.gameHand = []
        self.initSocket()

    def initSocket(self, serverHost="127.0.0.1", serverPort=12345):
        self.socket = socket.socket()
        self.socket.connect((serverHost, serverPort))
        print("Successfully connected, waiting for lobby")

    def startListening(self):
        self.playerId = int(self.socket.recv(1024).decode())
        print("Game started as bot, client id: {}".format(self.playerId))
        
        while True:
            i = "NOT IMPLEMENTED; BOT DATA HERE"
            self.socket.send(i.encode())
            data = self.socket.recv(MAX_DATA_SIZE).decode()
            print(data)