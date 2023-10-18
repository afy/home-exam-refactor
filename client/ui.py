from shared.constants import *

# <<Helper>> class
# Responsible for client-side display, client.player.Player class only
class UI:
    def __init__(self): pass


    # Display appropriate view given the JSON data from the client
    def show(self, data : dict):
        print("FROM UI: {}, {}".format(data, type(data)))


    # Debug logging
    def log(self, msg : str):
        print("LOG: {}".format(msg))