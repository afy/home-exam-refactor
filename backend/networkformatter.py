from shared.constants import *

# Format game state into JSON data that is sent to each client for UI, state mgmt and so on
# Contains game data (hands and drafts) aswell as visuals like scores.
# Used in the base class backend.boomerang.BoomerangGame
class NetworkFormatter:
    def __init__(self):
        pass

    def formatError(self, err, message):
        ret = self.constructBaseResponse(message)
        ret[KEY_JSON_DETAILS] = err
        return ret

    def formatInitial(self, player):
        ret = self.constructBaseResponse(MESSAGE_HANDSHAKE)
        ret[KEY_JSON_ID] = player.id
        ret[KEY_JSON_PLAYER_HAND] = self.parseCardList(player.hand)
        return ret

    # All rounds are over
    def formatGameOver(self):
        return self.constructBaseResponse()

    # Round has ended (one card remaining)
    def formatRoundEnd(self, players):
        return self.constructBaseResponse()

    # Default mid-round format
    def formatRound(self, players):
        ret = self.constructBaseResponse()
        for player in players:
            ret[player.id] = self.formatIndividualRound(player)
        return ret

    def formatIndividualRound(self, player):
        ret = self.constructBaseResponse()
        ret[KEY_JSON_GAMESTATE] = GAME_STATE_MID_ROUND
        ret[KEY_JSON_PLAYER_HAND] = self.parseCardList(player.hand)
        ret[KEY_JSON_PLAYER_DRAFT] = self.parseCardList(player.draft)
        return ret
    
    def parseCardList(self, cl):
        ret = []
        for e in cl:
            ret.append(e.code)
        return ret
    
    def constructBaseResponse(self, message=MESSAGE_NORMAL):
        return {KEY_JSON_MESSAGE: message}