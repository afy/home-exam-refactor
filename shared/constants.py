MAX_RECV_SIZE = 2048 # Maximum bytes sent over single TCP packet
DEFAULT_SERVER_PORT = 12345 
DEFAULT_SERVER_ADDRESS = '' 
LOCALHOST_CONNECT_ADDR = "127.0.0.1" # used in clients on localhost

# Game states
GAME_STATE_MID_ROUND = 0
GAME_STATE_ROUND_CATCH = 1
GAME_STATE_OVER = 2

# Message types (over TCP)
MESSAGE_HANDSHAKE = 0 # initial call; id + draft
MESSAGE_NORMAL = 1
MESSAGE_INVALID_INPUT = 2  # Client has entered invalid data to the server

# JSON Keys
KEY_JSON_MESSAGE = "message"
KEY_JSON_ID = "id"
KEY_JSON_PLAYER_HAND = "hand"
KEY_JSON_PLAYER_DRAFT = "draft"
KEY_JSON_DETAILS = "details"
KEY_JSON_GAMESTATE = "state"