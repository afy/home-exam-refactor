from backend.boomerang import BoomerangGame
from backend.objects.card import Card
from backend.objects.playerdata import PlayerData

from shared.custom_exceptions import *
from shared.gamestates import *


# Example implementation of the BoomerangGame class,
# Following the Boomerang Australia ruleset
class BoomerangAustralia(BoomerangGame): 
    def __init__(self, overrideDeckGeneration = False):
        super().__init__(_logname = "BoomerangAustralia")
        self.regionsVisited = {}
        if not overrideDeckGeneration:
            self.generateDeckInfo()
            

    # Overridden from BoomerangGame
    def makeBotDecision(self, bot : PlayerData) -> None:
        if self.gameState == GAME_STATE_ACTIVITY_SELECTION:

            # Select first activity if possible
            if len(bot.activities) > 0 and bot.activities[0] not in bot.activityUsed:
                bot.activitySelected = 0
                bot.activityUsed.append(bot.activities[0])

        elif self.gameState == GAME_STATE_MID_ROUND:
            playedCard = bot.hand[0]
            bot.hand.remove(playedCard)
            bot.draft.append(playedCard)


    # Overridden from BoomerangGame
    def calculateRoundScore(self) -> None:
        lockSites = [] # Sites to lock at the end of round
        regionsCompleted = [] # Bonus points to hand out at end of round

        for player in self.players:
            cards = player.hand + player.draft

            # ====================================== Throw and catch score
            throwCatchScore = abs(cards[0].number - cards[len(cards)-1].number)
            if throwCatchScore > player.highestThrowScore:
                player.highestThrowScore = throwCatchScore
            
            # ====================================== Tourist sites score
            regionScore = 0
            for c in cards:

                # Find region card is in
                region = None
                for rk, rv in self.regions.items():
                    if c.touristSite in rv:
                       region = rk
                       break

                if region == None: raise Boomerang_UndefinedLogicError("No region to associate to the site")
                
                # If a region is not locked
                site = self.regionsVisited[region]["Sites"][c.touristSite]
                if site[1] == False: 
                    lockSites.append(self.regionsVisited[region]["Sites"][c.touristSite])  
                    site[0].append(player.id)
                    regionScore += 1

                    # Check region cleared
                    cleared = True
                    for regSite in self.regionsVisited[region]["Sites"]:
                        if player.id not in self.regionsVisited[region]["Sites"][regSite][0]:
                            cleared = False
                            break
                    if cleared:
                        if len(self.regionsVisited[region]["Completed"]) == 0:
                            regionsCompleted.append([player, region])
            
            # ====================================== Collections score
            collValues = {
                "Leaves": 1,
                "Wildflowers": 2,
                "Shells": 3,
                "Souvenirs": 5
            }
            collectionScore = 0
            for c in cards:
                if c.collection != '':
                    collectionScore += collValues[c.collection]

            # ====================================== Animals score
            animals = {
                "Kangaroos": 3,
                "Emus": 4,
                "Wombats": 5,
                "Koalas": 7,
                "Platypuses": 9
            }
            animalScore = 0
            counts = {"Kangaroos": 0, "Emus": 0, "Wombats": 0, "Koalas": 0, "Platypuses": 0}
            for c in cards:
                if c.animal in animals.keys():
                    counts[c.animal] += 1
            for ak, av in animals.items():
                if ak in counts:
                    animalScore += (counts[ak] % 2) * av

            # ====================================== Activities score
            activityCount = 0
            scoreTable = {
                "0":0,
                "1":0,
                "2":2,
                "3":4,
                "4":7,
                "5":10,
                "6":12
            }
            for c in cards:
                if c.activity == player.activitySelected and activityCount < 7:
                    activityCount += 1
            activityScore = scoreTable[str(activityCount)]
            player.activities = [] # Reset activites for next round

            # ====================================== Tally up all scores
            if collectionScore <= 7:
                player.score += collectionScore * 2
            else:
                player.score += throwCatchScore + collectionScore + animalScore + activityScore + regionScore
        
        # ====================================== Bonus scores (After other counts)
        for site in lockSites:
            site[1] = True

        for regionInfo in regionsCompleted:
            player = regionInfo[0]
            region = regionInfo[1]
            self.regionsVisited[region]["Completed"].append(player)
            player.score += 3
            


    # Overridden from BoomerangGame
    def calculateWinner(self) -> int:
        maxScore = 0
        winners = []
        for player in self.players:
            if player.score > maxScore:
                winners = [player]
            if player.score == maxScore:
                winners.append(player)
        if len(winners) == 1: return winners[0].id

        # On tie
        elif len(winners) > 1:
            maxThrowScore = winners[0].score    
            winnerid = winners[0].id 
            for player in winners: 
                if player.highestThrowScore > maxThrowScore:
                    maxThrowScore = player.highestThrowScore
                    winnerid = player.id
            return winnerid


    # Overridden from BoomerangGame
    def runRound(self, clientInputBuffer : dict) -> None:
        self.log("Running round, gamestate {}".format(self.gameState))

        # Activity selection has been completed
        if self.gameState == GAME_STATE_ACTIVITY_SELECTION:
            for player in self.players: 

                # Add activity to calculations after round if any exist
                if not player.isBot and clientInputBuffer[player.id].upper() != "X":
                    player.activitySelected = int(clientInputBuffer[player.id])
                    activity = player.activities[player.activitySelected]
                    if activity not in player.activityUsed:
                        player.activityUsed.append(activity)

                # Remove final card, causing round to end after this runRound call
                finalCard = player.hand[0]
                player.hand.remove(finalCard)
                player.draft.append(finalCard)

            # Reset game state to normal execution
            self.gameState = GAME_STATE_MID_ROUND
            return

        # Update decks and drafts depending on move
        for playerId, move in clientInputBuffer.items():
            player = self.getPlayerById(int(playerId))
            playedCard = self.getCardInHand(player, move)
            player.hand.remove(playedCard)
            player.draft.append(playedCard)

        # Sample a random hand size; all users have the same size
        currentHandSize = len(self.players[0].hand) 

        # Rotate cards   
        if currentHandSize > 1:
            lp = len(self.players)-1
            savedDecks = [self.players[lp].hand]
            for i in range(0, lp):
                savedDecks.append(self.players[i].hand)
            for j in range(0, lp+1):
                self.players[j].hand = savedDecks[j]
            self.gameState = GAME_STATE_MID_ROUND

        # One card left, change mode to activity selection
        if currentHandSize == 1:
            self.gameState = GAME_STATE_ACTIVITY_SELECTION
            for player in self.players:
                for card in player.draft + player.hand:
                    if card.activity != '' and card.activity not in player.activityUsed:
                        player.activities.append(card.activity)


    # Overridden from BoomerangGame
    def validateClientInput(self, clientInput : dict, playerId : int) -> bool:
        try:
            player = self.getPlayerById(playerId)
        except Boomerang_UserNotFoundByIdException:
            self.log("In validate: Invalid playerId. Returning false")
            return False

        if self.gameState == GAME_STATE_ACTIVITY_SELECTION:
            if clientInput.upper() == "X":
                return True

            try: 
                clientInput = int(clientInput)
            except ValueError:
                return False
        
            player = self.getPlayerById(playerId)
            if clientInput < 0 or clientInput > len(player.activities)-1: # Invalid input range
                return False
            return True


        elif self.gameState == GAME_STATE_MID_ROUND:
            for c in player.hand:
                if c.code == str(clientInput).upper():
                    return True
        else:
            raise Boomerang_UndefinedLogicError
        return False


    def generateDeckInfo(self) -> None:
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

        # Valid data
        self.regions = {
            'Western Australia': ['The Bungle Bungles', 'The Pinnacles', 'Margaret River', 'Kalbarri National Park'],
            'Northern Territory': ['Uluru', 'Kakadu National Park', 'Nitmiluk National Park', "King's Canyon"], 
            'Queensland': ['The Great Barrier Reef', 'The Whitsundays', 'Daintree Rainforest', 'Surfers Paradise'], 
            'South Australia': ['Barossa Valley', 'Lake Eyre', 'Kangaroo Island', 'Mount Gambier'], 
            'New South Whales': ['Blue Mountains', 'Sydney Harbour', 'Bondi Beach', 'Hunter Valley'] ,
            'Victoria': ['Melbourne', 'The MCG', 'Twelve Apostles', 'Royal Exhibition Building', 'Salamanca Markets'], 
            'Tasmania': ['Mount Wellington', 'Port Arthur', 'Richmond']
        }
        self.codes = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '*', '-']
        self.collections = ['Leaves', '', 'Shells', 'Wildflowers', 'Souvenirs']
        self.animals = ['', 'Kangaroos', 'Emus', 'Wombats', 'Platypuses', 'Koalas']
        self.activities = ['Indigenous Culture', 'Sightseeing', '', 'Bushwalking', 'Swimming']

        # For region scoring
        for region, sites in self.regions.items():
            self.regionsVisited[region] = {}
            self.regionsVisited[region]["Completed"] = []
            self.regionsVisited[region]["Sites"] = {}
            for site in sites:
                self.regionsVisited[region]["Sites"][site] = [[], False] # ( Visited by players , Locked from visiting )
            