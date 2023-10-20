import unittest
import math
import copy

import backend.boomerang
import backend.server
import backend.boomerangaus

from shared.constants import *
from shared.custom_exceptions import *


# Note: not all requirements can be tested
# Additionally, the time ran out :(
# Requirements covered in test cases below:
# 1, 2, 3, 4, 5, 6, 8

class RequirementTesting(unittest.TestCase):
    # Requirement 1: server must host between 2 and 4 players
    def testServerArgs(self):
        self.assertRaises(Boomerang_InvalidArgException, backend.server.Server, 1, 0, True, False)
        self.assertRaises(Boomerang_InvalidArgException, backend.server.Server, 5, 0, True, False)
        backend.server.Server(2, 0, preventSocketStart=True, logging=False)
        backend.server.Server(3, 0, preventSocketStart=True, logging=False)
        backend.server.Server(4, 0, preventSocketStart=True, logging=False)


    # Requirement 2: A deck should consist on 28 valid cards
    # Requirement 3: Cards should be shuffled
    # Builtin list.shuffle() can produce same output in places
    # So allow for some flexibility
    def testDeck(self):
        game = backend.boomerangaus.BoomerangAustralia()
        self.assertEqual(len(game.deck), 28)
        validRegions = {
            'Western Australia': ['The Bungle Bungles', 'The Pinnacles', 'Margaret River', 'Kalbarri National Park'],
            'Northern Territory': ['Uluru', 'Kakadu National Park', 'Nitmiluk National Park', "King's Canyon"], 
            'Queensland': ['The Great Barrier Reef', 'The Whitsundays', 'Daintree Rainforest', 'Surfers Paradise'], 
            'South Australia': ['Barossa Valley', 'Lake Eyre', 'Kangaroo Island', 'Mount Gambier'], 
            'New South Whales': ['Blue Mountains', 'Sydney Harbour', 'Bondi Beach', 'Hunter Valley'] ,
            'Victoria': ['Melbourne', 'The MCG', 'Twelve Apostles', 'Royal Exhibition Building'], 
            'Tasmania': ['Salamanca Markets', 'Mount Wellington', 'Port Arthur', 'Richmond']
        }
        validCodes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '*', '-']
        validCollections = ['', 'Leaves' , 'Shells', 'Wildflowers', 'Souvenirs']
        validAnimals = ['', 'Kangaroos', 'Emus', 'Wombats', 'Platypuses', 'Koalas']
        validActivities = ['', 'Indigenous Culture', 'Sightseeing', 'Bushwalking', 'Swimming']
        for card in game.deck:
            self.assertTrue(card.region in validRegions.keys())
            self.assertTrue(card.touristSite in validRegions[card.region])
            self.assertTrue(card.code in validCodes)
            self.assertTrue(card.collection in validCollections)
            self.assertTrue(card.animal in validAnimals)
            self.assertTrue(card.activity in validActivities)   
        arr1 = copy.deepcopy(game.deck)
        game.shuffleDeck()
        arr2 = copy.deepcopy(game.deck)
        n = 0
        for i in range(0, len(game.deck)):
            if arr1[i].code == arr2[i].code:
                n += 1
        self.assertTrue(n < math.log2(len(game.deck)))    


    # Requirement 4: Deal 7 cards to each player
    # Requirement 6: Hand is passed along
    # Requirement 8: Continue 6 and 7 until only one card remains (combined with manual testing)
    def testGameLogic(self):
        s = backend.server.Server(4, 4, preventSocketStart=True, logging=False)
        s.startListening() # Bot only game; no sockets
        bots = s.game.getBots()

        # Requirment 4
        self.assertEqual(len(s.game.getBots()[0].hand), 7) 
        
        # Requirement 5
        hand1 = copy.deepcopy(bots[0].hand[1:8])
        hand2 = copy.deepcopy(bots[1].hand[1:8])
        hand3 = copy.deepcopy(bots[2].hand[1:8])
        hand4 = copy.deepcopy(bots[3].hand[1:8])
        s.game.makeBotDecision(bots[0], setCardDecision=bots[0].hand[0].code)
        s.game.makeBotDecision(bots[1], setCardDecision=bots[1].hand[0].code)
        s.game.makeBotDecision(bots[2], setCardDecision=bots[2].hand[0].code)
        s.game.makeBotDecision(bots[3], setCardDecision=bots[3].hand[0].code)
        s.game.runRound({})
        for i in range(5):
            self.assertEqual(hand1[i].code, bots[1].hand[i].code)
            self.assertEqual(hand2[i].code, bots[2].hand[i].code)
            self.assertEqual(hand3[i].code, bots[3].hand[i].code)
            self.assertEqual(hand4[i].code, bots[0].hand[i].code)

        # Requirement 8
        for j in range(5):
            s.game.makeBotDecision(bots[0], setCardDecision=bots[0].hand[0].code)
            s.game.makeBotDecision(bots[1], setCardDecision=bots[1].hand[0].code)
            s.game.makeBotDecision(bots[2], setCardDecision=bots[2].hand[0].code)
            s.game.makeBotDecision(bots[3], setCardDecision=bots[3].hand[0].code)


if __name__ == "__main__":
    unittest.main()