class GaduGaduServer():
    def __init__(self, socketServer):
        self.socketServer = socketServer
        self.users_list = []
       
       
    def Process(self):
      rcvData = self.socketServer.CheckForMsg()
      for socket,data in rcvData:
          parsedData = data.split(":",1)
          if parsedData[0] == "LOGIN":
            self.priv_process_login(socket, parsedData[1])
          elif parsedData[0] == "MSG_TO":
            self.priv_process_msg_to(socket,parsedData[1])

    def priv_process_login(self, socket, data):
        self.users_list.append((socket,data))
        dataToSend = "USERS:";
        nickList = []
        socketList = []
        for socket,nick in self.users_list:
            nickList.append(nick)
            socketList.append(socket)
        dataToSend += ",".join(nickList)
        
        for socket in socketList:
            self.socketServer.SendTo(socket,dataToSend)

    def priv_process_msg_to(self,socket,data):
        nick_from = ""
        for socket_from,nick in self.users_list:
            if socket_from == socket:
                nick_from = nick
                break
        
        socket_to_send = None
        parsedMsg = data.split(":",1)
        for socket_to,nick in self.users_list:
            if parsedMsg[0] == nick:
                socket_to_send = socket_to
                break
        if socket_to_send != None:
            self.socketServer.SendTo(socket_to_send,"MSG_FROM:" + nick_from + ":" + parsedMsg[1])
        else:
            self.socketServer.SendTo(socket,"MSG_ERROR:" + parsedMsg[0] + " not logged")
            