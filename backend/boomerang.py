import random

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
        self.deck = []
        

    def onPlayerConnect(self, playerId, maxReached):
        if self.playing: return -1
        playerId = int(playerId)

        self.log("added player, {}, {}".format(playerId, maxReached))

        if not maxReached:
            self.players[playerId] = {
                "hand": [],
                "draft": [],
                "score": 0
            }
        else:
            self.startGame()

    def runRound(self, clientInputBuffer):
        self.log(clientInputBuffer)
        responseBuffer = {}

        # update decks and drafts depending on move
        for playerId, move in clientInputBuffer.items():
            playerId = int(playerId)

            newDraft = self.players[playerId]["hand"].pop(move)
            self.players[playerId]["draft"][newDraft["key"]] = newDraft

        # rotate cards
        
        # update round score
        #if (playerId[])

        # if last round,
        if (self.rounds >= self.maxRound):
            responseBuffer = self.endGame()
        else:
            responseBuffer = self.networkFormatter.formatRound(self.players)

        return responseBuffer
    

    def startGame(self):
        self.playing = True
        self.log("Game started")
        self.fillDeck()
        self.shuffleDeck()
        self.handoutCards()
        self.round = 0

    def endGame(self):
        self.playing = False
        self.log("Game over")
        self.calculateFinalScore()
        return self.networkFormatter.formatGameOver()
        
    def shuffleDeck(self):
        random.shuffle(self.deck)

    def handoutCards(self):
        for i in range(0, len(self.players)):
            print(i)

    def fillDeck(self):
        self.deck.append("test card here")

    def calculateRoundScore(self):
        pass

    def calculateFinalScore(self):
        pass
    
    def log(self, msg):
        print("[BoomerangAustralia]: {}".format(msg))