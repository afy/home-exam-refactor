from client.client import Client
from client.ui import UI
from shared.constants import *
from shared.custom_exceptions import Boomerang_NetworkError

# Client controlled by the user; handles input/print logic
class Player(Client):
    def __init__(self, addr):
        super().__init__(addr)
        self.ui = UI()
        self.initSocket()

    def onInputRequired(self):
        self.ui.log(self.gameHand)
        print("->")
        i = input()
        if input != '':
            if i.upper() not in self.gameHand:
                self.ui.log("Invalid input. Please select a card from your hand by the code (\"A\" to \"-\")")
                return None
            else:
                return i

    def onResponse(self, data):
        self.ui.show(data)
        self.gameHand = data[KEY_JSON_PLAYER_HAND]

    def onLog(self, msg):
        self.ui.log(msg)

    def onInitialConnect(self, data):
        self.ui.log(data)
        self.ui.log("Game started, playing as player {} with hand".format(self.playerId, self.gameHand))