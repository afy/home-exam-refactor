from client.client import Client
from client.ui import UI

from shared.constants import *
from shared.jsonkeys import KEY_JSON_GAMESTATE, KEY_JSON_PLAYER_HAND, KEY_JSON_MESSAGE, KEY_JSON_ACTIVITY_LIST
from shared.gamestates import GAME_STATE_GAME_OVER, GAME_STATE_ACTIVITY_SELECTION
from shared.custom_exceptions import Boomerang_UnidentifiedMessage, Boomerang_NetworkError

# Client controlled by the user; handles input/print logic
class Player(Client):
    def __init__(self, addr):
        super().__init__()
        self.ui = UI()
        self.inputMode = "normal"
        self.activities = []
        self.activityInput = []
        self.initSocket(addr)


    # Overridden from Client
    def onResponse(self, data : dict) -> None:
        msg = data[KEY_JSON_MESSAGE]
        if msg == MESSAGE_NORMAL:
            if data[KEY_JSON_GAMESTATE] == GAME_STATE_GAME_OVER:
                self.ui.showGameOver(data)
                return

            elif data[KEY_JSON_GAMESTATE] == GAME_STATE_ACTIVITY_SELECTION:
                if len(data[KEY_JSON_ACTIVITY_LIST]) == 0: # No available options
                    self.inputMode = "skip"
                    return

                self.inputMode = "activity"
                self.activities = data[KEY_JSON_ACTIVITY_LIST]
                self.activityInput = []
                for i in range(0, len(self.activities)):
                    self.activityInput.append(str(i))
                self.ui.showActivitySelection(data, self.activities)
                return
            
            else:
                self.inputMode = "normal"
                self.gameHand = data[KEY_JSON_PLAYER_HAND]
                self.ui.show(data)

        elif MESSAGE_INVALID_INPUT:
            self.ui.log("Invalid input; Try again")
        elif MESSAGE_HANDSHAKE:
            raise Boomerang_NetworkError("No handshake messages should be sent at this time")
        else:
            raise Boomerang_UnidentifiedMessage("Message type is undefined")


    # Overridden from Client
    def onInputRequired(self) -> str:
        if self.inputMode == "skip":
            print("No activities to pick from, skipping turn... ")
            return "X" # No selection

        self.ui.showPlaintext("->")
        i = input()
        if input != '':
            if self.inputMode == "normal":
                if i.upper() not in self.gameHand:
                    self.ui.showPlaintext("Please select a card from your hand by the code (\"A\" to \"-\")")
                    return ""
                else:
                    self.ui.showPlaintext("Waiting for other players...")
                    return i
                
            elif self.inputMode == "activity":
                if i.upper() not in self.activityInput and i.upper() != "X":
                    self.ui.showPlaintext("Please select a valid activity index or skip with \"X\"")
                    return ""
                else:
                    self.ui.showPlaintext("Waiting for other players...")
                    return i
                

    # Overridden from Client
    def onSocketConnect(self) -> None:
        self.ui.showPlaintext("Connectied to server, waiting for other players")


    # Overridden from Client
    def onServerAccepted(self, data : dict) -> None:
        self.ui.displayOnConnect(data)
        