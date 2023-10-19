from shared.constants import *
from shared.custom_exceptions import Boomerang_UndefinedLogicError

# <<Helper>> class
# Responsible for client-side display, client.player.Player class only
class UI:
    def __init__(self): 
        self.divider = "=" * 20 
        self.divider += " "


    # Called on connect
    def displayOnConnect(self, data : dict):
        print("Game started, playing as player {} with hand {}".format(data[KEY_JSON_PLAYER_ID], data[KEY_JSON_PLAYER_HAND]))


    def showGameOver(self, data : dict):
        if data[KEY_JSON_GAMESTATE] == GAME_STATE_GAME_OVER:
            print(self.divider + "Game Over!")
            print("Scores:")
            print("You scored {} points!".format(data[KEY_JSON_PLAYER_SCORE]))
            maxScore, winnerId = data[KEY_JSON_PLAYER_SCORE], data[KEY_JSON_PLAYER_ID]
            for pid, pdata in data[KEY_JSON_OTHER_PLAYER_DATA].items():
                if pdata[KEY_JSON_OTHER_PLAYER_SCORE] > maxScore:
                    maxScore = pdata[KEY_JSON_OTHER_PLAYER_SCORE]
                    winnerId = pid
                print("Player {} scored {} points".format(pid, pdata[KEY_JSON_OTHER_PLAYER_SCORE]))

            # Player won
            if winnerId == data[KEY_JSON_PLAYER_ID]:
                print("You won the game!")

            else:
                print("Player {} won the game!".format(winnerId))

        else:
            raise Boomerang_UndefinedLogicError("onGameOver has been called but the game is still ongoing")


    # Display appropriate view given the JSON data from the client
    def show(self, data : dict):
        if data[KEY_JSON_GAMESTATE] == GAME_STATE_NEW_ROUND:
            print(self.divider + "New Round ({}/{})".format(
                data[KEY_JSON_ROUND_NUMBER], data[KEY_JSON_ROUND_TOTAL]
            ))
            print("Draft: {}".format(data[KEY_JSON_PLAYER_DRAFT]))
            print("Hand: {}".format(data[KEY_JSON_PLAYER_HAND]))
            self.printOtherPlayerHands(data[KEY_JSON_OTHER_PLAYER_DATA])
            

        elif data[KEY_JSON_GAMESTATE] == GAME_STATE_MID_ROUND:
            print("Draft: {}".format(data[KEY_JSON_PLAYER_DRAFT]))
            print("Hand: {}".format(data[KEY_JSON_PLAYER_HAND]))
            self.printOtherPlayerHands(data[KEY_JSON_OTHER_PLAYER_DATA])
            


    def printOtherPlayerHands(self, data : dict):
        print(data)
        for id in data:
            print("Player {} draft: {}".format(id, data[id][KEY_JSON_OTHER_PLAYER_DRAFT]))


    # Debug logging
    def log(self, msg : str):
        print("LOG: {}".format(msg))