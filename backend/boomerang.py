from backend.iboomerang import IBoomerang
from backend.inetwork import INetwork
from backend.networkformatter import NetworkFormatter

class BoomerangAustralia(IBoomerang, INetwork):
    def __init__(self):
        super().__init__()
        self.networkFormatter = NetworkFormatter()
        self.players = {}
        self.playing = False
        self.round = 0
        self.maxRound = 4
        

    def onPlayerConnect(self, id, maxReached):
        if self.playing: return -1

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

        for playerId, move in clientInputBuffer.items():
            playerId = int(playerId)
            
            # ...

            responseBuffer[playerId]

        return responseBuffer

    def startGame(self):
        self.log("Game started")
        self.shuffleDeck()
        self.handoutCards()
        self.round = 0
        

    def shuffleDeck(self):
        pass

    def handoutCards(self):
        pass

    def calculateScore(self):
        self.playing = True
        raise NotImplementedError
    
    def log(self, msg):
        print("GAME: {}".format(msg))