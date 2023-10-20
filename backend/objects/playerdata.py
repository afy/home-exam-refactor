# Store player state in backend.boomerang.BoomerangGame
class PlayerData:
    def __init__(self, _id, bot = False):
        self.id = _id
        self.hand = []
        self.draft = []
        self.score = 0
        self.highestThrowScore = 0 # For determining winner at ties
        self.isBot = bot

        self.activities = [] # Activities for latest round
        self.activitySelected = None # For this round
        self.activityUsed = []