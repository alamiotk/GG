from SocketServer import SocketServer
from CheckInput import CheckInput
server = SocketServer()

print ("Enter exit to close server!")
while True :
    server.CheckForNewClient()
    server.ProcessClients()
    MESSAGE = CheckInput()
    if MESSAGE == 'exit':
        break
