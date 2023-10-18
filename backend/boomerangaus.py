from backend.boomerang import BoomerangGame
from backend.card import Card

from shared.custom_exceptions import *

class BoomerangAustralia(BoomerangGame): 
    def __init__(self):
        super().__init__(_logname="BoomerangAustralia")
        self.generateDeckInfo()

    # @Override as required by parent class
    def calculateRoundScore(self):
        self.log("CalculateScoreCall")
    
    # @Override as required by parent class
    def calculateFinalScore(self):
        self.log("CalculateFinalScoreCall")

    # @Override as required by parent class
    def validateClientInput(self, input):
        self.log("{}, {}".format(input, str(input).upper() in self.codes))
        return str(input).upper() in self.codes


    # @Override as required by parent class
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
    


    def generateDeckInfo(self):
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
        self.codes = []
        for c in self.deck:
            self.codes.append(c.code)