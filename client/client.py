import socket
import json

from shared.constants import *
from shared.custom_exceptions import Boomerang_NetworkError

# Abstract class
# Defines network behaviour for clients (player and bots)
class Client:
    def __init__(self, addr):
        super().__init__()
        self.playerId = None
        self.gameHand = []



    # Requires override
    def onResponse(self, data : dict):
        raise NotImplementedError
    
    # Requires override
    # returns message to send
    def onInputRequired(self):
        raise NotImplementedError
    
    # Requires override
    def onLog(self, msg : str):
        raise NotImplementedError
    
    # requires override 
    def onInitialConnect(self, data : dict):
        raise NotImplementedError
    


    def initSocket(self, serverAddr=LOCALHOST_CONNECT_ADDR, serverPort=DEFAULT_SERVER_PORT):
        self.socket = socket.socket()
        self.socket.connect((serverAddr, serverPort))
        self.onLog("Successfully connected, waiting for lobby")


    def startListening(self):
        initialData = json.loads(self.socket.recv(MAX_RECV_SIZE).decode())
        if initialData[KEY_JSON_MESSAGE] != MESSAGE_HANDSHAKE:
            raise Boomerang_NetworkError("First message from server must be a handshake")

        self.playerId = int(initialData[KEY_JSON_ID])
        self.gameHand = initialData[KEY_JSON_PLAYER_HAND]
        self.onInitialConnect(initialData)
        
        while True:
            msg = self.onInputRequired()
            if msg != None:
                self.socket.send(msg.encode())
                data = self.socket.recv(MAX_RECV_SIZE).decode()
                self.onResponse(json.loads(data))