import random
import traceback

from backend.iboomerang import IBoomerang
from backend.inetwork import INetwork
from backend.networkformatter import NetworkFormatter
from backend.card import Card
from backend.playerdata import PlayerData

from shared.custom_exceptions import *

class BoomerangAustralia:#(IBoomerang, INetwork):
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
        if self.playing: raise NotImplementedError()
        playerId = int(playerId)

        self.log("added player, {}, {}".format(playerId, maxReached))

        self.players.append(PlayerData(playerId))
        if maxReached:
            self.startGame()

    # Run when all clients have submitted an action
    def runRound(self, clientInputBuffer):
        responseBuffer = {}

        # update decks and drafts depending on move
        for playerId, move in clientInputBuffer.items():
            self.log("{}, {}".format(playerId, move))
            player = self.getPlayerById(int(playerId))
            playedCard = self.getCardInHand(player, move)
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
        if (self.round >= self.maxRound):
            responseBuffer = self.endGame()
        else:
            responseBuffer = self.networkFormatter.formatRound(self.players)

        self.log("Response: {}".format(responseBuffer))
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

    def getInitalValues(self, playerId):
        return self.networkFormatter.formatInitial(self.getPlayerById(int(playerId)))

    def handoutCards(self):
        for i in range(0, len(self.players)):
            for j in range(0, 7):
                if len(self.deck) > 0:
                    card = self.deck.pop(random.randrange(len(self.deck)))
                    self.players[i].hand.append(card)
                else:
                    print("Out of cards in deck")
                    break

    def fillDeck(self):
        self.deck.append(Card("The Bungle Bungles","A","Western Australia", 1, "Leaves", "", "Indigenous Culture"))
        self.deck.append(Card("The Pinnacles","B","Western Australia", 1, "", "Kangaroos", "Sightseeing"))
        self.deck.append(Card("Margaret River","C","Western Australia", 1, "Shells", "Kangaroos", ""))
        self.deck.append(Card("Kalbarri National Park","D","Western Australia", 1, "Wildflowers", "", "Bushwalking"))
        self.deck.append(Card("Uluru","E","Northern Territory", 4, "", "Emus", "Indigenous Culture"))
        self.deck.append(Card("Kakadu National Park","F","Northern Territory", 4, "", "Wombats", "Sightseeing"))
        self.deck.append(Card("Nitmiluk National Park","G","Northern Territory", 4, "Shells", "Platypuses", "")) 
        self.deck.append(Card("King's Canyon","H","Northern Territory", 4, "", "Koalas", "Swimming"))
        self.deck.append(Card("The Great Barrier Reef","I","Queensland", 6, "Wildflowers", "", "Sightseeing"))
        self.deck.append(Card("The Whitsundays","J","Queensland", 6, "", "Kangaroos", "Indigenous Culture"))
        self.deck.append(Card("Daintree Rainforest","K","Queensland", 6, "Souvenirs", "", "Bushwalking"))
        self.deck.append(Card("Surfers Paradise","L","Queensland", 6, "Wildflowers", "", "Swimming"))
        self.deck.append(Card("Barossa Valley","M","South Australia", 3, "", "Koalas", "Bushwalking"))
        self.deck.append(Card("Lake Eyre","N","South Australia", 3, "", "Emus", "Swimming"))
        self.deck.append(Card("Kangaroo Island","O","South Australia", 3, "", "Kangaroos", "Bushwalking"))
        self.deck.append(Card("Mount Gambier","P","South Australia", 3, "Wildflowers", "", "Sightseeing"))
        self.deck.append(Card("Blue Mountains","Q","New South Whales", 5, "", "Wombats", "Indigenous Culture"))
        self.deck.append(Card("Sydney Harbour","R","New South Whales", 5, "", "Emus", "Sightseeing"))
        self.deck.append(Card("Bondi Beach","S","New South Whales", 5, "", "Wombats", "Swimming"))
        self.deck.append(Card("Hunter Valley","T","New South Whales", 5, "", "Emus", "Bushwalking"))
        self.deck.append(Card("Melbourne","U","Victoria", 2, "", "Wombats", "Bushwalking"))
        self.deck.append(Card("The MCG","V","Victoria", 2, "Leaves", "", "Indigenous Culture"))
        self.deck.append(Card("Twelve Apostles","W","Victoria", 2, "Shells", "", "Swimming"))
        self.deck.append(Card("Royal Exhibition Building","X","Victoria", 2, "Leaves", "Platypuses", ""))	 
        self.deck.append(Card("Salamanca Markets","Y","Tasmania", 7, "Leaves", "Emus", ""))
        self.deck.append(Card("Mount Wellington","Z","Tasmania", 7, "", "Koalas", "Sightseeing"))
        self.deck.append(Card("Port Arthur","*","Tasmania", 7, "Leaves", "", "Indigenous Culture"))
        self.deck.append(Card("Richmond","-","Tasmania", 7, "", "Kangaroos", "Swimming"))
        self.regions = ["Western Australia", "Northern Territory", "Queensland", "South Australia", "New South Whales", "Victoria", "Tasmania"]

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
        raise Boomerang_UserNotFoundByIdException
    
    def getCardInHand(self, player, code):
        for c in player.hand:
            if c.code == code.upper(): return c
        raise Boomerang_CardNotFoundByCodeException