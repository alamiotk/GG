import socket
import select
class SocketClient():
    def __init__(self, server_ip = "127.0.0.1", server_port = 5001):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((server_ip, server_port))
        except socket.error:
            print ("SocketClient connection error")

    def Send(self, StringData):
        try:
            self.sock.send(StringData.encode())
        except socket.error:
            print ("SocketClient connection error")

    def Receive(self, timeout = 0.2):
        data = ""
        try:
            readable, writable, errored = select.select([self.sock], [], [], timeout)
            for toRead in readable:
                data = toRead.recv(1024)
        except socket.error:
            print ("SocketClient connection error")
        return data

    def __del__(self):
        try:
            self.sock.close()
        except socket.error:
            print ("SocketClient connection error")