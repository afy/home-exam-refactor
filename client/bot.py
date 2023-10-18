import socket

from client.iclient import IClient
from shared.constants import *

# Automated player
class Bot(IClient):
    def __init__(self):
        super().__init__()
        self.playerId = None
        self.gameHand = []
        self.initSocket()

    def initSocket(self, serverAddr=DEFAULT_SERVER_ADDRESS, serverPort=DEFAULT_SERVER_PORT):
        self.socket = socket.socket()
        self.socket.connect((serverAddr, serverPort))
        print("Successfully connected, waiting for lobby")

    def startListening(self):
        self.playerId = int(self.socket.recv(MAX_RECV_SIZE).decode())
        print("Game started as bot, client id: {}".format(self.playerId))
        
        while True:
            i = "NOT IMPLEMENTED; BOT DATA HERE"
            self.socket.send(i.encode())
            data = self.socket.recv(MAX_RECV_SIZE).decode()
            print(data)