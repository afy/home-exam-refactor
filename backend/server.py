# Thanks to
# https://stackoverflow.com/questions/23828264/how-to-make-a-simple-multithreaded-socket-server-in-python-that-remembers-client

import socket
import threading
import traceback
import json

from shared.constants import *
from backend.boomerangaus import BoomerangAustralia

# Handles network communication to/from clients over socket TCP
# Communicates with the game logic over backend.inetwork.INetwork interface
class Server: 
    def __init__(self, numberClients : int, numberBots : int):
        # Replace with any Boomerang game class
        # Must inherit and fully implement backend.
        self.game = BoomerangAustralia() 

        self.log("Initialized server with {} players and {} bots".format(numberClients, numberBots))
        self.gameStarted = False
        self.clients = []
        self.maxConnections = int(numberClients)
        self.currentId = 0
        self.gameLock = threading.Lock()
        self.clientInputBuffer = {}
        self.gameResponseBuffer = {}
        self.initSocket()
        
    def initSocket(self, address=DEFAULT_SERVER_ADDRESS, port=DEFAULT_SERVER_PORT):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((address, port))
        
    # Await initial connections. Stops when all slots have been filled (self.maxConnections)
    def startListening(self):
        self.socket.listen(self.maxConnections)
        while True:
            client, address = self.socket.accept()
            self.clients.append(client)
            finalPlayer = len(self.clients) >= self.maxConnections
            self.game.onPlayerConnect(self.currentId, finalPlayer)
            if finalPlayer:
                self.log("Starting game")
                self.game.startGame()
                self.gameStarted = True
            threading.Thread(target = self.listenToClient,args = (client, address, self.currentId)).start()
            self.currentId += 1

    # Runs in a separate thread, one per client connection
    def listenToClient(self, client, address, playerId):
        while not self.gameStarted: pass
        self.gameLock.acquire()
        client.send(json.dumps(self.game.getInitalValues(playerId)).encode())
        self.gameLock.release()

        while True:
            try:
                self.threadPrint(address, playerId, "Waiting for client response")
                data = client.recv(MAX_RECV_SIZE).decode()
                self.threadPrint(address, playerId, "Response recieved")

                if data:

                    self.gameLock.acquire()
                    if not self.game.validateClientInput(data): 
                        self.threadPrint(address, playerId, "Invalid input; Asking to try again")
                        client.send(json.dumps({
                            "message": "invalid message"
                        }).encode())
                    self.gameLock.release()

                    # Write client input to shared buffer
                    self.gameLock.acquire()
                    self.clientInputBuffer[playerId] = data
                    if len(self.clientInputBuffer) >= self.maxConnections:
                        self.gameResponseBuffer = self.game.runRound(self.clientInputBuffer)
                        self.clientInputBuffer = {}
                    self.gameLock.release()

                    # Wait for all buffers to write
                    i = 0
                    while len(self.clientInputBuffer) < self.maxConnections:
                        if len(self.clientInputBuffer) == 0: # buffer has been cleared
                            break
                        if i == 0: 
                            self.threadPrint(address, playerId, "Waiting for other threads.. ({}/{})".format(len(self.clientInputBuffer), self.maxConnections))
                            i = 1

                    # Send back info from responseBuffer (see Boomerang class)
                    self.threadPrint(address, playerId, "Responding to client")
                    response = self.gameResponseBuffer[playerId]
                    client.send(json.dumps(response).encode())
                    self.gameResponseBuffer.pop(playerId)

                else:
                    self.log("DANGER DANGER DANGER DANGER")
                    raise Exception("No data was sent to the server")
                    #sys.exit()
                    
            except Exception as e:
                self.log("Exception in thread, closing connection: {} [{}] \n{}".format(e, repr(e), traceback.print_exc()))
                client.close()
                return False
            
    def threadPrint(self, address, playerId, msg):
        print("[Server t{}: to {}]: {}".format(playerId, address, msg))  

    def log(self, msg):
        print("[Server]: {}".format(msg))