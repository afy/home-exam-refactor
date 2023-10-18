import json

class UI:
    def __init__(self):
        pass

    # Display appropriate view given the JSON data from the client
    def showData(self, data):
        print("FROM UI \""+json.loads(data)+"\"")