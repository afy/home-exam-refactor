import socket

from client.iclient import IClient
from client.ui import UI

MAX_DATA_SIZE = 1024 # bytes
 
class Player(IClient):
    def __init__(self, addr):
        super().__init__()
        self.ui = UI()
        self.address = addr
        self.playerId = None
        self.gameHand = []
        self.initSocket()

    def initSocket(self, serverHost="127.0.0.1", serverPort=12345):
        self.socket = socket.socket()
        self.socket.connect((serverHost, serverPort))
        print("Successfully connected, waiting for lobby")

    def startListening(self):
        self.playerId = int(self.socket.recv(1024).decode())
        print("Game started, playing as player {}".format(self.playerId))
        
        while True:
            print("->")
            i = input()
            if input != '':
                self.socket.send(i.encode())
                data = self.socket.recv(MAX_DATA_SIZE).decode()
                UI.show(data)