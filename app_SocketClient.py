from SocketClient import SocketClient
from CheckInput import CheckInput
client = SocketClient()

print("Enter 'exit' to close client")
msg = ""
nick = input("Enter your nick: ")

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
