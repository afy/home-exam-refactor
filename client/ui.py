from shared.constants import *

class UI:
    def __init__(self): pass

    # Display appropriate view given the JSON data from the client
    def show(self, data : dict):
        print("FROM UI: {}, {}".format(data, type(data)))

    # Debug logging
    def log(self, msg : str):
        print("LOG: {}".format(msg))