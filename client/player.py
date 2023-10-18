import socket

from client.iclient import IClient
from client.ui import UI
from shared.constants import *

# Client controlled by the user; handles input/print logic
class Player(IClient):
    def __init__(self, addr):
        super().__init__()
        self.ui = UI()
        self.address = addr
        self.playerId = None
        self.gameHand = []
        self.initSocket()

    def initSocket(self, serverAddr=DEFAULT_SERVER_ADDRESS, serverPort=DEFAULT_SERVER_PORT):
        self.socket = socket.socket()
        self.socket.connect((serverAddr, serverPort))
        print("Successfully connected, waiting for lobby")

    def startListening(self):
        self.playerId = int(self.socket.recv(MAX_RECV_SIZE).decode())
        print("Game started, playing as player {}".format(self.playerId))
        
        while True:
            print("->")
            i = input()
            if input != '':
                self.socket.send(i.encode())
                data = self.socket.recv(MAX_RECV_SIZE).decode()
                UI.show(data)