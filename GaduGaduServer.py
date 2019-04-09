class GaduGaduServer():
    def __init__(self, socketServer):
        self.socketServer = socketServer
       
       
    def Process(self):
      rcvData = self.socketServer.CheckForMsg()
      for toSend in rcvData:
        self.socketServer.SendToAll(toSend)