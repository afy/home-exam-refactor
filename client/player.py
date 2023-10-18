import socket
import json

from client.iclient import IClient
from client.ui import UI
from shared.constants import *
from shared.custom_exceptions import Boomerang_NetworkError

# Client controlled by the user; handles input/print logic
class Player:#(IClient):
    def __init__(self, addr):
        super().__init__()
        self.ui = UI()
        self.playerId = None
        self.gameHand = []
        self.initSocket()

    def initSocket(self, serverAddr=LOCALHOST_CONNECT_ADDR, serverPort=DEFAULT_SERVER_PORT):
        self.socket = socket.socket()
        self.socket.connect((serverAddr, serverPort))
        self.ui.log("Successfully connected, waiting for lobby")

    def startListening(self):
        initialData = json.loads(self.socket.recv(MAX_RECV_SIZE).decode())
        if initialData[KEY_JSON_MESSAGE] != MESSAGE_HANDSHAKE:
            raise Boomerang_NetworkError("First message from server must be a handshake")

        self.playerId = int(initialData[KEY_JSON_ID])
        self.gameHand = initialData[KEY_JSON_PLAYER_HAND]
        self.ui.log("Game started, playing as player {} with hand".format(self.playerId, self.gameHand))
        
        while True:
            print("->")
            i = input()
            if input != '':
                if i.upper() not in self.gameHand:
                    self.ui.log("Invalid input. Please select a card from your hand by the code (\"A\" to \"-\")")
                else:
                    self.socket.send(i.encode())
                    data = self.socket.recv(MAX_RECV_SIZE).decode()
                    self.ui.show(data)