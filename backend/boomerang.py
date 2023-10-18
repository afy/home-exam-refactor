import random

from backend.iboomerang import IBoomerang
from backend.inetwork import INetwork
from backend.networkformatter import NetworkFormatter
from backend.card import Card
from backend.playerdata import PlayerData

from tools.custom_exceptions import Boomerang_UserNotFoundById

class BoomerangAustralia(IBoomerang, INetwork):
    def __init__(self):
        super().__init__()
        self.networkFormatter = NetworkFormatter()
        self.players = []
        self.playing = False
        self.round = 0
        self.maxRound = 4
        self.deck = []      

    # Run when server authenticates a connection, maxReached
    # indicates if the server has a full lobby
    def onPlayerConnect(self, playerId, maxReached):
        if self.playing: return -1
        playerId = int(playerId)

        self.log("added player, {}, {}".format(playerId, maxReached))

        if not maxReached:
            self.players.append(PlayerData(playerId))
        else:
            self.startGame()

    # Run when all clients have submitted an action
    def runRound(self, clientInputBuffer):
        self.log(clientInputBuffer)
        responseBuffer = {}

        # update decks and drafts depending on move
        for playerId, move in clientInputBuffer.items():
            player = self.getPlayerById(int(playerId))
            playedCard = self.getCardByCode(player, move)
            player.hand.remove(playedCard)
            player.draft.append(playedCard)

        # rotate cards
        
        # update round score
        # all users have same #cards, so check first one for round end
        if len(self.players[0].hand) > 1:
            pass # swap normal

        elif len(self.players[0].hand) == 1:
            pass # swap back and then end round (special output)

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

    # Calculate score for each player at the end of a round
    def calculateRoundScore(self):
        pass

    # Calculate score for each player at the end of the game
    def calculateFinalScore(self):
        pass
    
    def log(self, msg):
        print("[BoomerangAustralia]: {}".format(msg))

    def getPlayerById(self, id):
        for p in self.players:
            if p.id == id: return p
        raise Boomerang_UserNotFoundById
    
    def getCardByCode(self, player, code):
        for c in player.cards:
            if c.code == code: return c
        raise 