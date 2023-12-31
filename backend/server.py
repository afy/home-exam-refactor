# Thanks for basic socket server structure:
# https://stackoverflow.com/questions/23828264/how-to-make-a-simple-multithreaded-socket-server-in-python-that-remembers-client


import socket
import threading
import traceback
import json
import sys

from backend.boomerangaus import BoomerangAustralia

from shared.constants import *
from shared.gamestates import GAME_STATE_GAME_OVER
from shared.jsonkeys import KEY_JSON_PLAYER_RETURN_DICT, KEY_JSON_GAMESTATE
from shared.custom_exceptions import Boomerang_InvalidArgException, Boomerang_NetworkError

# Handles network communication to/from clients over socket TCP
# Communicates with the game logic over backend.inetwork.INetwork interface
class Server: 
    def __init__(self, numberClients : int, numberBots : int, preventSocketStart : bool = False, logging : bool = True):
        numberClients, numberBots = self.parseArgs(numberClients, numberBots)
        self.logging = logging

        # Replace with any Boomerang game class
        # Must inherit and fully implement backend.boomerang.BoomerangGame.
        self.game = BoomerangAustralia(logging = self.logging) 

        # Initialize bots
        self.currentId = 0
        for i in range(0, numberBots):
            self.game.addBot(self.currentId)
            self.currentId += 1

        self.log("Initialized server with {} players and {} bots".format(numberClients, numberBots))
        self.gameStarted = False
        self.running = True
        self.clients = []
        self.gameLock = threading.Lock()
        self.clientLock = threading.Lock()
        self.clientInputBuffer = {}
        self.gameResponseBuffer = {}
        self.maxConnections = numberClients - numberBots
        if not preventSocketStart and self.maxConnections > 0: self.initSocket()
        

    def initSocket(self, address=DEFAULT_SERVER_ADDRESS, port=DEFAULT_SERVER_PORT) -> None:
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((address, port))
        

    # Await initial connections. Stops when all slots have been filled (self.maxConnections)
    def startListening(self) -> None:
        
        # All bot game. Prevent connections
        if self.maxConnections == 0:
            self.game.startGame()
            return

        self.socket.listen(self.maxConnections)
        while self.running:
            client, address = self.socket.accept()
            self.clients.append(client)
            maxReached = len(self.clients) >= self.maxConnections
            self.game.onPlayerConnect(self.currentId, maxReached)  
            threading.Thread(target = self.listenToClient,args = (client, address, self.currentId)).start()
            if maxReached:
                self.log("Lobby is full")
                self.game.startGame()
                self.gameStarted = True
                break
            self.currentId += 1


    # Runs in a separate thread, one per client connection
    def listenToClient(self, client, address, playerId : int) -> None:
        while not self.gameStarted: pass
        self.gameLock.acquire()
        client.send(json.dumps(self.game.getInitialValues(playerId)).encode())
        self.gameLock.release()

        while True and self.running:
            try:
                self.threadPrint(address, playerId, "Waiting for client response")
                data = client.recv(MAX_RECV_SIZE).decode()
                self.threadPrint(address, playerId, "Response recieved")
                if data:

                    self.gameLock.acquire()
                    if not self.game.validateClientInput(data, playerId): 
                        self.threadPrint(address, playerId, "Invalid input; Asking to try again")
                        client.send(json.dumps({
                            "message": "invalid message"
                        }).encode())
                        self.gameLock.release()
                        continue
                    self.gameLock.release()

                    # Write client input to shared buffer
                    self.gameLock.acquire()
                    self.clientInputBuffer[playerId] = data

                    # All clients have made their selection; run game tick
                    if len(self.clientInputBuffer) >= self.maxConnections:
                        self.gameResponseBuffer = self.game.onAllClientInputLogged(self.clientInputBuffer)
                        self.clientInputBuffer = {}
                    self.gameLock.release()

                    # Wait for all buffers to write
                    # "i" insures it only prints once
                    i = 0
                    while len(self.clientInputBuffer) < self.maxConnections:
                        if len(self.clientInputBuffer) == 0: # Buffer has been cleared
                            break
                        if i == 0: 
                            self.threadPrint(address, playerId, "Waiting for other threads.. ({}/{})".format(len(self.clientInputBuffer), self.maxConnections))
                            i = 1

                    # Send back info from responseBuffer (see Boomerang class)
                    self.threadPrint(address, playerId, "Responding to client")
                    self.gameLock.acquire()
                    response = self.gameResponseBuffer[KEY_JSON_PLAYER_RETURN_DICT][playerId]
                    gameOver = response[KEY_JSON_GAMESTATE] == GAME_STATE_GAME_OVER
                    self.gameResponseBuffer[KEY_JSON_PLAYER_RETURN_DICT].pop(playerId)
                    self.gameLock.release()
                    client.send(json.dumps(response).encode())

                    if gameOver:
                        self.threadPrint(address, playerId, "Detected game over message from boomerang, closing socket + thread.")
                        client.close()
                        self.clientLock.acquire()
                        self.clients.remove(client)

                        # This thread is the last listener, close program
                        if len(self.clients) <= 0:
                            self.stop() 
                        self.clientLock.release()
                        sys.exit()                
                else:
                    raise Boomerang_NetworkError("No data was sent to the server")
                    
            except Exception as e:
                self.log("Caught exception in thread, closing connection and shutting off thread:\n {} [{}] \n{}".format(e, repr(e), traceback.print_exc()))
                client.close()
                self.clientLock.acquire()
                self.clients.remove(client)

                # This thread is the last listener, close program
                if len(self.clients) <= 0:
                    self.stop() 
                self.clientLock.release()
                sys.exit()


    def threadPrint(self, address, playerId : int, msg : str) -> None:
        if not self.logging: return
        print("[Server t{}: to {}]: {}".format(playerId, address, msg))  


    def log(self, msg : str) -> None:
        if not self.logging: return
        print("[Server]: {}".format(msg))


    def stop(self) -> None:
        self.log("Closing connection and exiting all threads")
        self.running = False
        self.socket.close()


    def parseArgs(self, clients : int, bots : int) -> tuple:
        try:
            clients = int(clients)
        except ValueError:
            raise Boomerang_InvalidArgException("#Clients cant be converted to int")
        
        if clients < 2 or clients > 4:
            raise Boomerang_InvalidArgException("#Clients must be between 2 and 4")
        
        try:
            bots = int(bots)
        except ValueError:
            raise Boomerang_InvalidArgException("#Bots cant be converted to int")
        
        if bots < 0 or bots > clients:
            raise Boomerang_InvalidArgException("#Bots must be > 0 and <= #clients")
        
        return clients, bots