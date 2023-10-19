from shared.constants import *

# <<Helper>> class
# Responsible for client-side display, client.player.Player class only
class UI:
    def __init__(self): 
        self.divider = "="*10


    # Called on connect
    def displayOnConnect(self, data : dict):
        print("Game started, playing as player {} with hand {}".format(data[KEY_JSON_PLAYER_ID], data[KEY_JSON_PLAYER_HAND]))


    # Display appropriate view given the JSON data from the client
    def show(self, data : dict):
        print("FROM UI: {}, {}".format(data[KEY_JSON_GAMESTATE], data))
        if data[KEY_JSON_GAMESTATE] == GAME_STATE_NEW_ROUND:
            print(self.divider + "New round")
            print("Draft: {}".format(data[KEY_JSON_PLAYER_DRAFT]))
            print("Hand: {}".format(data[KEY_JSON_PLAYER_HAND]))

        elif data[KEY_JSON_GAMESTATE] == GAME_STATE_MID_ROUND:
            print("Draft: {}".format(data[KEY_JSON_PLAYER_DRAFT]))
            print("Hand: {}".format(data[KEY_JSON_PLAYER_HAND]))


    # Debug logging
    def log(self, msg : str):
        print("LOG: {}".format(msg))