from SocketServer import SocketServer
from CheckInput import CheckInput
from GaduGaduServer import GaduGaduServer
server = SocketServer()
ggServer = GaduGaduServer(server)
print ("Enter exit to close server!")
while True :
    server.CheckForNewClient()
    ggServer.Process()
    MESSAGE = CheckInput()
    if MESSAGE == 'exit':
        break
