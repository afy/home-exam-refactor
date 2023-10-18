import json

class NetworkFormatter:
    def __init__(self):
        pass

    def formatGameOver():
        pass

    def formatRound(self, players):
        ret = {}
        for player in players:
            ret[player.id] = self.formatIndividualRound(player)
        return ret

    def formatIndividualRound(self, player):
        ret = {}
        ret["newHand"] = []
        ret[""] = []
        return ret