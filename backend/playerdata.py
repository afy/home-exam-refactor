# Store player state in backend.boomerang.BoomerangGame
class PlayerData:
    def __init__(self, _id):
        self.id = _id
        self.hand = []
        self.draft = []
        self.score = 0
