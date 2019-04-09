class GaduGaduClient():
    def __init__(self, socketClient):
        self.socketClient = socketClient
       
       
    def Login(self, nick):
        self.socketClient.Send("LOGIN:" + nick)