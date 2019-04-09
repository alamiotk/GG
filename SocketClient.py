import socket
import select
class SocketClient():
    def __init__(self, server_ip = "127.0.0.1", server_port = 5001):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((server_ip, server_port))

    def Send(self, StringData):
        self.sock.send(StringData.encode())

    def Receive(self, timeout = 0.2):
        readable, writable, errored = select.select([self.sock], [], [], timeout)
        for toRead in readable:
            return toRead.recv(1024)
        return ""

    def __del__(self):
        self.sock.close()