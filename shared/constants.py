# Global-scope constants

MAX_RECV_SIZE = 2048 # Maximum bytes sent over single TCP packet
DEFAULT_SERVER_PORT = 12345 
DEFAULT_SERVER_ADDRESS = '' 
LOCALHOST_CONNECT_ADDR = "127.0.0.1" # used in clients on localhost

# Message types (over TCP)
MESSAGE_HANDSHAKE = 0 # initial call; id + draft
MESSAGE_NORMAL = 1
MESSAGE_INVALID_INPUT = 2  # Client has entered invalid data to the server