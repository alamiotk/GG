class GaduGaduClient():
    def __init__(self, socketClient):
        self.socketClient = socketClient
        self.nick = ""
       
       
    def Login(self, nick):
        self.socketClient.Send("LOGIN:" + nick)
        self.nick = nick
    def SendMsg(self,msg):
        data = msg.split(":",1)
        if len(data) == 2:
            self.socketClient.Send("MSG:" + self.nick + ":" + data[0] + ":" + data[1])
        else:
            print("Wybierz do kogo chcesz wysłać wiadomość poprzez nick: 'Twoja wiadomosc'")