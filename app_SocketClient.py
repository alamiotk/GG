import sys
from SocketClient import SocketClient
from CheckInput import CheckInput
from GaduGaduClient import GaduGaduClient
server_ip_address = "127.0.0.1"
if len(sys.argv) >= 2:
    server_ip_address = sys.argv[1]

client = SocketClient(server_ip_address)
ggClient = GaduGaduClient(client)
print("Enter 'exit' to close client")
nick = input("Enter your nick: ")
ggClient.Login(nick)
print("You can chat with your friends")
while True:
    msg = CheckInput()
    if msg == 'exit':
        break
    if "" != msg:
        ggClient.SendMsg(msg)
    data = client.Receive()
    if "" != data:
        print (data.decode())
