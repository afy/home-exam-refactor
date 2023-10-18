from client.client import Client
from shared.constants import *

# Automated player
class Bot(Client):
    def __init__(self):
        super().__init__()
        self.initSocket()


    def onResponse(self, data : dict) -> None:
        print(data)
        self.gameHand = data[KEY_JSON_PLAYER_HAND]


    def onInputRequired(self) -> str:
        # Make a random guess / logic / predefined behaviour
        return ""


    def onLog(self, msg : str) -> None:
        print(msg)


    def onInitialConnect(self, data : dict) -> None:
        print(data)
        print("Game started, playing as player {} with hand".format(self.playerId, self.gameHand))