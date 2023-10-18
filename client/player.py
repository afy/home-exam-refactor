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

    def onResponse(self, data : dict) -> None:
        self.ui.show(data)
        self.gameHand = data[KEY_JSON_PLAYER_HAND]

    def onInputRequired(self) -> str:
        self.ui.log(self.gameHand)
        print("->")
        i = input()
        if input != '':
            if i.upper() not in self.gameHand:
                self.ui.log("Invalid input. Please select a card from your hand by the code (\"A\" to \"-\")")
                return ""
            else:
                return i



    def onLog(self, msg : str) -> None:
        self.ui.log(msg)

    def onInitialConnect(self, data : dict) -> None:
        self.ui.log(data)
        self.ui.log("Game started, playing as player {} with hand".format(self.playerId, self.gameHand))