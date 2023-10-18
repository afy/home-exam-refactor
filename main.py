import sys
from backend.server import Server
from client.player import Player
from tools.custom_exceptions import BA_InvalidArgLengthException

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
                    raise BA_InvalidArgLengthException


# program entry point
if __name__ == "__main__":
     Main()