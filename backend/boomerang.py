from abc import ABC, abstractmethod
import random

from backend.inetwork import INetwork
from backend.helpers.networkformatter import NetworkFormatter
from backend.objects.playerdata import PlayerData

from shared.custom_exceptions import *
from shared.gamestates import *


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
        self.gameState = GAME_STATE_NOT_STARTED


    # Required override
    # Calculate score for each player at the end of a round
    # Updates self.players
    @abstractmethod
    def calculateRoundScore(self) -> None:
        raise NotImplementedError

    # Required override
    # Calculate score for each player at the end of the game
    # Return id of winner
    @abstractmethod
    def calculateWinner(self) -> int:
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
    
    # Required override
    # Make a decision for bots (serverside)
    def makeBotDecision(self, bot : int) -> None:
        raise NotImplementedError
    
    



    # Overridden from INetwork
    def addBot(self, id : int) -> None:
        if self.playing: raise Boomerang_NetworkError("Bot cant be added while game is in session")

        # Confirm enough cards have been defined 
        # Called ONLY on first connection
        if len(self.players) == 0:
            if len(self.deck) < self.minDeckSize:
                raise Boomerang_NotEnoughCardsException("Please define more cards for the game")

        bot = PlayerData(int(id), bot=True)
        self.players.append(bot)
        self.handoutCards(bot)
    

    # Overridden from INetwork
    def onAllClientInputLogged(self, clientInputBuffer : dict) -> None:
        hasBeenReset = False # If True, round has reset (round end met)
        for bot in self.getBots():
            self.makeBotDecision(bot)

         # Update game state 
        self.runRound(clientInputBuffer) 

        # Round over
        if len(self.players[0].hand) == 0:
            self.calculateRoundScore()
            self.round += 1
            self.resetDeck()
            self.shuffleDeck()
            for player in self.players:
                self.handoutCards(player)
            hasBeenReset = True

        # Last round
        if (self.round > self.maxRound):
            self.calculateRoundScore()
            return self.endGame(self.calculateWinner())         
        if hasBeenReset:
            return self.networkFormatter.formatNewRound(self.players, self.round, self.maxRound)
        if self.gameState == GAME_STATE_ACTIVITY_SELECTION:
            return self.networkFormatter.formatActivityRound(self.players)  
        return self.networkFormatter.formatRound(self.players, self.round, self.maxRound)


    # Overridden from INetwork
    # Run when server authenticates a connection
    # maxReached indicates if the server has a full lobby INCLUDING the new player
    def onPlayerConnect(self, playerId : int, maxReached : bool) -> None:
        if self.playing: raise Boomerang_NetworkError("Player cant connect while game is in session")

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
    def startGame(self) -> None:
        self.playing = True
        self.log("Game started")
        self.shuffleDeck()
        self.round = 1
        self.gameState = GAME_STATE_MID_ROUND
        

    # Overridden from INetwork
    def getInitialValues(self, playerId : int) -> None:
        return self.networkFormatter.formatInitial(self.getPlayerById(int(playerId)))
    

    


    # Called when last round has been played
    # Must return a formatted view from networkFormatter
    def endGame(self, winnerId : int):
        self.playing = False
        self.log("Game over")
        return self.networkFormatter.formatGameOver(self.players, winnerId)
        

    def shuffleDeck(self) -> None:
        random.shuffle(self.deck)


    def resetDeck(self) -> None:
        for player in self.players:
            self.deck = self.deck + player.hand + player.draft
            player.hand = []
            player.draft = []
                


    # Hand out cards to singular player
    # Called from onPlayerConnect
    def handoutCards(self, player : PlayerData) -> None:
        for i in range(0, self.handSize):
            if len(self.deck) > 0:
                card = self.deck.pop(0)
                player.hand.append(card)
            else:
                raise Boomerang_UndefinedLogicError("Not enough cards in deck to hand out")


    def log(self, msg : str) -> None:
        print("[{}]: {}".format(self.logname, msg))


    def getPlayerById(self, id : int) -> None:
        for p in self.players:
            if p.id == id: return p
        raise Boomerang_UserNotFoundByIdException
    

    def getCardInHand(self, player : PlayerData, code : str) -> None:
        for c in player.hand:
            if c.code == code.upper(): return c
        raise Boomerang_CardNotFoundByCodeException
    

    def getBots(self) -> list: 
        ret = []
        for player in self.players:
            if player.isBot: ret.append(player)
        return ret