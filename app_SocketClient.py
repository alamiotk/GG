from SocketClient import SocketClient
from CheckInput import CheckInput
from GaduGaduClient import GaduGaduClient
client = SocketClient()
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
        client.Send(nick + ": " + msg)
    data = client.Receive()
    if "" != data:
        print (data.decode())
