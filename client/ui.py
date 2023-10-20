from shared.jsonkeys import *
from shared.gamestates import *
from shared.custom_exceptions import Boomerang_UndefinedLogicError

# <<Helper>> class
# Responsible for client-side display, client.player.Player class only
class UI:
    def __init__(self): 
        self.largeDivider = ("=" * 30) + " "
        self.smallDivider = ("="*20) + " "


    # Called on connect
    def displayOnConnect(self, data : dict) -> None:
        print("Game started, playing as player {} with hand {}".format(data[KEY_JSON_PLAYER_ID], data[KEY_JSON_PLAYER_HAND]))


    def showGameOver(self, data : dict) -> None:
        if data[KEY_JSON_GAMESTATE] == GAME_STATE_GAME_OVER:
            print(self.largeDivider + "Game Over!")
            print("Scores:")
            print("You scored {} points!".format(data[KEY_JSON_PLAYER_SCORE]))
            winnerId = data[KEY_JSON_WINNER_ID]
            for pid, pdata in data[KEY_JSON_OTHER_PLAYER_DATA].items():
                print("Player {} scored {} points".format(pid, pdata[KEY_JSON_OTHER_PLAYER_SCORE]))

            if winnerId == data[KEY_JSON_PLAYER_ID]:
                print("You won the game!")
            else:
                print("\nPlayer {} won the game!".format(winnerId))
        else:
            raise Boomerang_UndefinedLogicError("onGameOver has been called but the game is still ongoing")


    # Display appropriate view given the JSON data from the client
    def show(self, data : dict) -> None:
        if data[KEY_JSON_GAMESTATE] == GAME_STATE_NEW_ROUND:
            print(self.largeDivider + "New Round ({}/{})".format(
                data[KEY_JSON_ROUND_NUMBER], data[KEY_JSON_ROUND_TOTAL]
            ))
            print("Draft: {}".format(data[KEY_JSON_PLAYER_DRAFT]))
            print("Hand: {}".format(data[KEY_JSON_PLAYER_HAND]))
            self.printOtherPlayerHands(data[KEY_JSON_OTHER_PLAYER_DATA])
            
        elif data[KEY_JSON_GAMESTATE] == GAME_STATE_MID_ROUND:
            print(self.smallDivider)
            print("Draft: {}".format(data[KEY_JSON_PLAYER_DRAFT]))
            print("Hand: {}".format(data[KEY_JSON_PLAYER_HAND]))
            self.printOtherPlayerHands(data[KEY_JSON_OTHER_PLAYER_DATA])


    def showActivitySelection(self, data : dict, activities : list) -> None:
        if data[KEY_JSON_GAMESTATE] == GAME_STATE_ACTIVITY_SELECTION:
            print(self.smallDivider)
            print("Select one activity from the list below. Input corresponding index (starting at one)")
            print("Input \"X\" instead to skip selection")
            print("Activities: {}".format(activities))
            

    def printOtherPlayerHands(self, data : dict) -> None:
        for id in data:
            print("Player {} draft: {}".format(id, data[id][KEY_JSON_OTHER_PLAYER_DRAFT]))


    def showPlaintext(self, msg : str) -> None:
        print(msg)

    # Debug logging
    def log(self, msg : str) -> None:
        print("     DEBUG LOG: {}".format(msg))