from shared.constants import *


# <<Helper>> class
# Format game state into JSON data that is sent over net to each client (for UI, state mgmt and so on)
# Contains game data (hands and drafts) aswell as visuals like scores.
# Used in the base class backend.boomerang.BoomerangGame
class NetworkFormatter:
    def __init__(self): pass


    def formatError(self, err, message):
        ret = self.constructBaseResponse(message)
        ret[KEY_JSON_DETAILS] = err
        return ret


    def formatInitial(self, player):
        ret = self.constructBaseResponse(MESSAGE_HANDSHAKE)
        ret[KEY_JSON_GAMESTATE] = GAME_STATE_NEW_ROUND
        ret[KEY_JSON_PLAYER_ID] = player.id
        ret[KEY_JSON_PLAYER_HAND] = self.parseCardList(player.hand)
        return ret
    

    def formatNewRound(self, players):
        return self.formatRound(players, roundState = GAME_STATE_NEW_ROUND)


    # All rounds are over
    def formatGameOver(self):
        ret = self.constructBaseResponse()
        ret[KEY_JSON_GAMESTATE] = GAME_STATE_GAME_OVER
        return ret


    # Called after runRound 
    def formatRound(self, players, roundState = GAME_STATE_MID_ROUND):
        ret = self.constructBaseResponse()
        ret[KEY_JSON_PLAYER_RETURN_DICT] = {}
        for player in players:
            ret[KEY_JSON_PLAYER_RETURN_DICT][player.id] = self.formatIndividualRound(player, players, roundState)
        return ret


    # Format individual return data ; what the client "sees"
    def formatIndividualRound(self, player, players, roundState):
        ret = self.constructBaseResponse()
        ret[KEY_JSON_GAMESTATE] = roundState
        ret[KEY_JSON_PLAYER_HAND] = self.parseCardList(player.hand)
        ret[KEY_JSON_PLAYER_DRAFT] = self.parseCardList(player.draft)
        ret[KEY_JSON_PLAYER_SCORE] = player.score
        ret[KEY_JSON_OTHER_PLAYER_DATA] = {}

        for other in players:
            if other.id != player.id:
                ret[KEY_JSON_OTHER_PLAYER_DATA][other.id] = {
                    KEY_JSON_OTHER_PLAYER_DRAFT: self.parseCardList(other.draft),
                    KEY_JSON_OTHER_PLAYER_SCORE: other.score
                }

        return ret
    

    # Parse lists of Card types into valid json format
    def parseCardList(self, cl):
        ret = []
        for e in cl:
            ret.append(e.code)
        return ret
    

    # use message=None for wrappers/internal
    def constructBaseResponse(self, message=MESSAGE_NORMAL):
        return {} if message==None else {KEY_JSON_MESSAGE: message}