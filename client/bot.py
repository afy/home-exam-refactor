import socket

from client.client import Client
from shared.constants import *

# Automated player
class Bot(Client):
    def __init__(self):
        super().__init__()

    def onInputRequired(self):
        # Make a random guess / logic / predefined behaviour
        return None

    def onResponse(self, data : dict):
        print(data)
        self.gameHand = data[KEY_JSON_PLAYER_HAND]

    def onLog(self, msg : str):
        print(msg)

    def onInitialConnect(self, data : dict):
        print(data)
        print("Game started, playing as player {} with hand".format(self.playerId, self.gameHand))