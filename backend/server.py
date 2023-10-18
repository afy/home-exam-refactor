import socket
import threading
import sys
import time
from backend.boomerang import BoomerangAustralia

# adapted from
# https://stackoverflow.com/questions/23828264/how-to-make-a-simple-multithreaded-socket-server-in-python-that-remembers-client


class Server: 
    def __init__(self, numberClients, numberBots):
        print("Initialized server with {} players and {} bots".format(numberClients, numberBots))
        self.game = BoomerangAustralia() # Replace with any Boomerang Game
        self.gameStarted = False
        self.clients = []
        self.maxConnections = int(numberClients)
        self.currentId = 0
        self.gameLock = threading.Lock()
        self.clientInputBuffer = {}
        self.gameResponseBuffer = {}
        self.initSocket()
        
    def initSocket(self, address='', port=12345):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((address, port))
        
    def startListening(self):
        self.socket.listen(self.maxConnections)
        while True:
            client, address = self.socket.accept()
            self.clients.append(client)
            finalPlayer = len(self.clients) >= self.maxConnections
            self.game.onPlayerConnect(self.currentId, finalPlayer)
            self.currentId += 1
            if finalPlayer:
                print("Starting game")
                self.game.startGame()
                self.gameStarted = True
            threading.Thread(target = self.listenToClient,args = (client, address, self.currentId)).start()

    def listenToClient(self, client, address, playerId):
        while not self.gameStarted: pass
        client.send(playerId.encode())

        while True:
            try:
                self.threadPrint(address, playerId, "Waiting for client response")
                data = client.recv(1024).decode()
                self.threadPrint(address, playerId, "Response recieved")

                if data:
                    self.gameLock.acquire()
                    self.clientInputBuffer[playerId] = data
                    if len(self.clientInputBuffer) >= self.maxConnections:
                        self.gameResponseBuffer = self.game.runRound(self.clientInputBuffer)
                        self.clientInputBuffer = {}
                    self.gameLock.release()

                    i = 0
                    while len(self.clientInputBuffer) < self.maxConnections:
                        if len(self.clientInputBuffer) == 0: # buffer has been cleared
                            break

                        if i == 0: 
                            self.threadPrint(address, playerId, "Waiting for other threads.. ({}/{})".format(len(self.clientInputBuffer), self.maxConnections))
                            time.sleep(2)
                            i = 0

                    self.threadPrint(address, playerId, "Responding to client")
                    response = self.gameResponseBuffer[playerId]
                    client.send(response.encode())
                    del self.gameResponseBuffer[playerId]
                else:
                    sys.exit()
                    
            except Exception as e:
                print("Exception in thread, closing connection: \"", e, "\"")
                client.close()
                return False
            
    def threadPrint(self, address, playerId, msg):
        print("[Server t{}: to {}]: {}".format(playerId, address, msg))  