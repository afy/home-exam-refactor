import json

from shared.constants import *

class UI:
    def __init__(self):
        pass

    # Display appropriate view given the JSON data from the client
    def show(self, data):
        if data == None:
            print("Cannot parse data")
            return
        data = json.loads(data)
        print("FROM UI [{}]:   \"{}\"".format(data, data[KEY_JSON_MESSAGE]))

    def log(self, msg):
        print("LOG: {}".format(msg))