import socket
import select

class SocketServer():
    def __init__(self, server_ip = "0.0.0.0", server_port = 5001):
        try:
            proto = socket.getprotobyname('TCP')
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto)
            self.sock.bind((server_ip, server_port))
            self.sock.listen(0)
            self.clientSocketList = []
        except socket.error:
            print ("SocketServer connection error")

    def CheckForNewClient(self, timeout = 0.2):
        try:
            readable, writable, errored = select.select([self.sock], [], [], timeout)
            for s in readable:
                (conn_sock, (ip,port)) = self.sock.accept()
                print ("SocketServer : New client handled: " + str(ip) + ":" + str(port))
                self.clientSocketList.append(conn_sock)
        except socket.error:
            print ("SocketServer connection error")

    def CheckForMsg(self, timeout = 0.2):
        data = []
        try:
            if self.clientSocketList:
                readable, writable, errored = select.select(self.clientSocketList, [], [], timeout)
                for toRead in readable:
                    try:
                        data.append((toRead,toRead.recv(1024).decode()))
                    except socket.error:
                        data.append((toRead,"ERROR"))
                        self.clientSocketList.remove(toRead)
                        toRead.close()
        except socket.error:
            print ("SocketServer connection error")
        return data

    def SendTo(self, socket, data):
        try:
            socket.send(data.encode())
        except socket.error:
            print ("SocketServer connection error")
        
    def __del__(self):
        try:
            for s in self.clientSocketList:
                s.close()
            self.sock.close()
        except socket.error:
            print ("SocketServer connection error")

