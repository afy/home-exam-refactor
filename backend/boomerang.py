import random

from backend.inetwork import INetwork
from backend.networkformatter import NetworkFormatter
from backend.playerdata import PlayerData
from shared.custom_exceptions import *
from backend.inetwork import INetwork

class BoomerangGame(INetwork):
    def __init__(self, _logname="Boomerang"):
        super().__init__()
        self.networkFormatter = NetworkFormatter()
        self.players = []
        self.playing = False
        self.round = 0
        self.maxRound = 4
        self.deck = []      
        self.logname = _logname


    # Required override
    # Calculate score for each player at the end of a round
    def calculateRoundScore(self):
        raise NotImplementedError

    # Required override
    # Calculate score for each player at the end of the game
    def calculateFinalScore(self):
        raise NotImplementedError

    # Required override
    # Runs when all clients have send valid input
    def runRound(self, clientInputBuffer):
        raise NotImplementedError
    
    # Requires override
    # Called from server to validate input
    def validateClientInput(self, input):
        raise NotImplementedError
    

    
    # Run when server authenticates a connection, maxReached
    # indicates if the server has a full lobby
    def onPlayerConnect(self, playerId, maxReached):
        if self.playing: raise NotImplementedError()
        playerId = int(playerId)
        player = PlayerData(playerId)
        self.players.append(player)
        self.handoutCards(player)

        self.log("added player, {}, {}".format(playerId, maxReached))
        if maxReached:
            self.startGame()


    def startGame(self):
        self.playing = True
        self.log("Game started")
        self.shuffleDeck()
        self.round = 0

    # Called when last round has been played
    # Must return a formatted view from networkFormatter
    def endGame(self):
        self.playing = False
        self.log("Game over")
        self.calculateFinalScore()
        return self.networkFormatter.formatGameOver()
        
    def shuffleDeck(self):
        random.shuffle(self.deck)

    def getInitalValues(self, playerId):
        return self.networkFormatter.formatInitial(self.getPlayerById(int(playerId)))

    # Hand out cards to player
    def handoutCards(self, player):
        for i in range(0, 7):
            if len(self.deck) > 0:
                card = self.deck.pop(random.randrange(len(self.deck)))
                player.hand.append(card)
            else:
                print("Out of cards in deck")
                break

    def log(self, msg):
        print("[{}]: {}".format(self.logname, msg))

    def getPlayerById(self, id):
        for p in self.players:
            if p.id == id: return p
        raise Boomerang_UserNotFoundByIdException
    
    def getCardInHand(self, player, code):
        for c in player.hand:
            if c.code == code.upper(): return c
        raise Boomerang_CardNotFoundByCodeException