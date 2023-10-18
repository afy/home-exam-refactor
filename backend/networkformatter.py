import json

from shared.constants import *

# Format game state into JSON data that is sent to each client
# Contains game data (hands and drafts) aswell as visuals like
# scores
class NetworkFormatter:
    def __init__(self):
        pass

    # All rounds are over
    def formatGameOver():
        pass

    # Round has ended (one card remaining)
    def formatRoundEnd(self, players):
        pass

    # Default mid-round format
    def formatRound(self, players):
        ret = {}
        for player in players:
            ret[player.id] = self.formatIndividualRound(player)
        return json.dumps(ret)

    def formatIndividualRound(self, player):
        ret = {}
        ret["state"] = GAME_STATE_MID_ROUND
        ret["hand"] = player.hand
        ret["draft"] = player.draft
        return ret