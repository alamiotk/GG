class GaduGaduServer():
    def __init__(self, socketServer):
        self.socketServer = socketServer
        self.users_list = []
       
       
    def Process(self):
      rcvData = self.socketServer.CheckForMsg()
      for data in rcvData:
          dataToSend = data
          parsedData = data.split(":",1)
          if parsedData[0] == "LOGIN":
            self.users_list.append(parsedData[1])
            dataToSend = "USERS:" + ",".join(self.users_list)
          self.socketServer.SendToAll(dataToSend)