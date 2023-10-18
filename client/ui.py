import json

class UI:
    def __init__(self):
        pass

    def showData(self, data):
        print("FROM UI \""+json.dumps(data)+"\"")