from backend.iboomerang import IBoomerang
from backend.inetwork import INetwork

class BoomerangAustralia(IBoomerang, INetwork):
    def __init__(self):
        super().__init__()
        self.players = {}
        self.playing = False

    def onPlayerConnect(self, id, maxReached):
        if self.playing: return

        self.log("added player, {}, {}".format(id, maxReached))

        if not maxReached:
            self.players[id] = {
                "hand": [],
                "draft": [],
                "score": 0
            }

        else:
            self.startGame()

    def runRound(self, clientInputBuffer):
        self.log(clientInputBuffer)
        responseBuffer = {}

        for k, v in clientInputBuffer.items():
            responseBuffer[k] = "Server echoes " + v

        return responseBuffer

    def startGame(self):
        pass #self.log("Game started")

    def calculateScore(self):
        self.playing = True
        raise NotImplementedError
    
    def log(self, msg):
        print("GAME: {}".format(msg))