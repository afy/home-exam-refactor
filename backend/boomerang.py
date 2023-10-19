import random
from abc import ABC, abstractmethod

from backend.inetwork import INetwork
from backend.helpers.networkformatter import NetworkFormatter
from backend.objects.playerdata import PlayerData
from shared.custom_exceptions import Boomerang_NotEnoughCardsException, Boomerang_UserNotFoundByIdException, Boomerang_CardNotFoundByCodeException, Boomerang_UndefinedLogicError
from backend.inetwork import INetwork

# <<Abstract>> class representing the various versions of Boomerang
# Any variant inherits and overrides from this class, and should then work with current system
class BoomerangGame(INetwork, ABC):
    def __init__(self, _logname="Boomerang"):
        super().__init__()
        self.networkFormatter = NetworkFormatter()
        self.players = []
        self.playing = False
        self.round = 1
        self.maxRound = 1
        self.minDeckSize = 28
        self.handSize = 3
        self.deck = []      
        self.logname = _logname


    # Required override
    # Calculate score for each player at the end of a round
    # Updates self.players
    @abstractmethod
    def calculateRoundScore(self) -> None:
        raise NotImplementedError

    # Required override
    # Calculate score for each player at the end of the game
    # Updates self.players
    @abstractmethod
    def calculateFinalScore(self) -> None:
        raise NotImplementedError

    # Required override
    # Runs when all clients have send valid input
    # Runs the game logic in regards to card swaps and similar
    @abstractmethod
    def runRound(self, clientInputBuffer : dict) -> None:
        raise NotImplementedError
    
    # Required override
    # Called from server to validate input
    @abstractmethod
    def validateClientInput(self, input : str, playerId : int) -> bool:
        raise NotImplementedError
    




    # Overridden from INetwork
    def onAllClientInputLogged(self, clientInputBuffer):
        hasBeenReset = False
        self.runRound(clientInputBuffer)  # Update game state 
        self.log(self.round)

        # Round over
        if len(self.players[0].hand) <= 1:
            self.calculateRoundScore()
            self.round += 1
            self.resetDeck()
            self.shuffleDeck()
            for player in self.players:
                self.handoutCards(player)
            hasBeenReset = True

        # Last round
        if (self.round > self.maxRound):
            self.calculateFinalScore()
            responseBuffer = self.endGame()    
        else:
            if hasBeenReset:
                responseBuffer = self.networkFormatter.formatNewRound(self.players, self.round, self.maxRound)
            else:
                responseBuffer = self.networkFormatter.formatRound(self.players, self.round, self.maxRound)

        return responseBuffer

    
    # Overridden from INetwork
    # Run when server authenticates a connection
    # maxReached indicates if the server has a full lobby INCLUDING the new player
    def onPlayerConnect(self, playerId, maxReached):
        if self.playing: raise NotImplementedError()

        # Confirm enough cards have been defined 
        # Called ONLY on first connection
        if len(self.players) == 0:
            if len(self.deck) < self.minDeckSize:
                raise Boomerang_NotEnoughCardsException("Please define more cards for the game")

        playerId = int(playerId)
        player = PlayerData(playerId)
        self.players.append(player)
        self.handoutCards(player)
        self.log("added player, {} {}".format(playerId, ", Full lobby" if maxReached else ""))


    # Overridden from INetwork
    def startGame(self):
        self.playing = True
        self.log("Game started")
        self.shuffleDeck()
        self.round = 1
        

    # Overridden from INetwork
    def getInitialValues(self, playerId):
        return self.networkFormatter.formatInitial(self.getPlayerById(int(playerId)))
    

    


    # Called when last round has been played
    # Must return a formatted view from networkFormatter
    def endGame(self):
        self.playing = False
        self.log("Game over")
        self.calculateFinalScore()
        return self.networkFormatter.formatGameOver(self.players)
        

    def shuffleDeck(self):
        pass #random.shuffle(self.deck)

    def resetDeck(self):
        for player in self.players:
            self.deck = self.deck + player.hand + player.draft
            player.hand = []
            player.draft = []
                


    # Hand out cards to singular player
    # Called from onPlayerConnect
    def handoutCards(self, player):
        for i in range(0, self.handSize):
            if len(self.deck) > 0:
                card = self.deck.pop(0)
                player.hand.append(card)
            else:
                raise Boomerang_UndefinedLogicError("Not enough cards in deck to hand out")


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