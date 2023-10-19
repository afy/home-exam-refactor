import sys
from backend.server import Server
from client.player import Player
from shared.custom_exceptions import Boomerang_InvalidArgException

class Main:
    def __init__(self):
            match len(sys.argv)-1:
                case 1:
                    player = Player(sys.argv[1])
                    player.startListening()
                case 2:
                    server = Server(sys.argv[1], sys.argv[2])
                    server.startListening() 
                case _:
                    raise Boomerang_InvalidArgException


# program entry point
if __name__ == "__main__":
     Main()