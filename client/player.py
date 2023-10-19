from client.client import Client
from client.ui import UI
from shared.constants import *
from shared.custom_exceptions import Boomerang_UnidentifiedMessage, Boomerang_NetworkError

# Client controlled by the user; handles input/print logic
class Player(Client):
    def __init__(self, addr):
        super().__init__(addr)
        self.ui = UI()
        self.initSocket()


    def onResponse(self, data : dict) -> None:
        if data[KEY_JSON_GAMESTATE] == GAME_STATE_GAME_OVER:
            self.ui.showGameOver(data)
            return

        msg = data[KEY_JSON_MESSAGE]
        if msg == MESSAGE_NORMAL:
            self.ui.show(data)
            self.gameHand = data[KEY_JSON_PLAYER_HAND]
        elif MESSAGE_INVALID_INPUT:
            self.ui.log("Invalid input; Try again")
        elif MESSAGE_HANDSHAKE:
            raise Boomerang_NetworkError("No handshake messages should be sent at this time")
        else:
            raise Boomerang_UnidentifiedMessage("Message type is undefined")


    def onInputRequired(self) -> str:
        print("->")
        i = input()
        if input != '':
            if i.upper() not in self.gameHand:
                self.ui.log("Please select a card from your hand by the code (\"A\" to \"-\")")
                return ""
            else:
                print("Waiting for other players..")
                return i


    def onLog(self, msg : str) -> None:
        self.ui.log(msg)


    def onInitialConnect(self, data : dict) -> None:
        self.ui.displayOnConnect(data)
        