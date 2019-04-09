import socket
import select

class SocketServer():
    def __init__(self, server_ip = "0.0.0.0", server_port = 5001):
        proto = socket.getprotobyname('TCP')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, proto)
        self.sock.bind((server_ip, server_port))
        self.sock.listen()
        self.clientSocketList = []

    def CheckForNewClient(self, timeout = 0.2):
        readable, writable, errored = select.select([self.sock], [], [], timeout)
        for s in readable:
            if s is self.sock:
                (conn_sock, (ip,port)) = self.sock.accept()
                print ("SocketServer : New client handled: " + str(ip) + ":" + str(port))
                self.clientSocketList.append(conn_sock)

    def ProcessClients(self, timeout = 0.2):
        if self.clientSocketList:
            readable, writable, errored = select.select(self.clientSocketList, [], [], timeout)
            for toRead in readable:
                data = toRead.recv(1024)
                for toSend in self.clientSocketList:
                    toSend.send(data)

    def __del__(self):
        for s in self.clientSocketList:
            s.close()
        self.sock.close()