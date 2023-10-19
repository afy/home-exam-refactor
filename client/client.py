import socket
import json
from abc import ABC, abstractmethod

from shared.constants import *
from shared.custom_exceptions import Boomerang_NetworkError

# <<Abstract>> class
# Defines network behaviour for clients (player and bots)
class Client(ABC):
    def __init__(self):
        super().__init__()
        self.playerId = None
        self.gameHand = []
        self.running = False


    # Required override
    @abstractmethod
    def onResponse(self, data : dict) -> None:
        raise NotImplementedError
    
    # Required override
    # returns message to send
    @abstractmethod
    def onInputRequired(self) -> str:
        raise NotImplementedError
    
    # Required override
    @abstractmethod
    def onLog(self, msg : str) -> None:
        raise NotImplementedError
    
    # required override 
    @abstractmethod
    def onInitialConnect(self, data : dict) -> None:
        raise NotImplementedError
    

    


    def initSocket(self, serverAddr=LOCALHOST_CONNECT_ADDR, serverPort=DEFAULT_SERVER_PORT):
        self.socket = socket.socket()
        self.socket.connect((serverAddr, serverPort))
        self.onLog("Successfully connected, waiting for lobby")


    def startListening(self):
        initialData = json.loads(self.socket.recv(MAX_RECV_SIZE).decode())
        if initialData[KEY_JSON_MESSAGE] != MESSAGE_HANDSHAKE:
            raise Boomerang_NetworkError("First message from server must be a handshake")

        self.playerId = int(initialData[KEY_JSON_PLAYER_ID])
        self.gameHand = initialData[KEY_JSON_PLAYER_HAND]
        self.onInitialConnect(initialData)
        
        self.running = True
        while self.running:
            msg = self.onInputRequired()
            if msg != "" and msg != None:
                self.socket.send(msg.encode())
                data = self.socket.recv(MAX_RECV_SIZE).decode()
                data = json.loads(data)
                if data[KEY_JSON_GAMESTATE] == GAME_STATE_GAME_OVER:
                    self.socket.close()
                    self.running = False

                self.onResponse(data)



