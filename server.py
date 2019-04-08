import socket
from threading import Thread
from datetime import datetime

TCP_IP = '0.0.0.0'
TCP_PORT = 2004
BUFFER_SIZE = 2048
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


def get_now():
    return datetime.now().strftime(DATETIME_FORMAT)


class Client(object):
    def __init__(self, client_socket, srv):
        """ Initializing Client.
        :param client_socket: Socket object
        :param srv: reference to server where connected is Client"""

        # Stop to stop thread
        self.stop = False

        self.client_socket = client_socket
        self.server = srv

        # Get name of client
        self.client_socket.send('Welcome! Type your nick and press enter!')
        self.name = self.client_socket.recv(BUFFER_SIZE).decode('utf-8')
        self.client_socket.send(
            'Welcome {}! If you want to quit write "EXIT"'.format(self.name)
        )

        # Send msg to all chat users
        self.server.broadcast("{} has joined chat!".format(self.name))

        # Add user to char user set
        self.server.clients.add(self)

    def process_message(self, msg):
        """
        Process message received from client.
        :param msg: decoded message
        """

        if msg == 'EXIT':
            self.client_socket.close()
            del self.server.clients[self]
            self.server.broadcast('{} has left.'.format(self.name))

        # Dodaje funkcjonalnosc z punktu 4
        elif msg == 'LIST':
            self.client_socket.send(
                "Currently on chat: " +
                ", ".join((client.name for client in self.server.clients))
            )

        else:
            self.server.broadcast(msg, self)

    def start_working_loop(self):
        """ Method should be started via thread. Waiting for message."""

        self.client_socket.settimeout(1)

        while not self.stop:
            try:
                msg = self.client_socket.recv(BUFFER_SIZE).decode('utf-8')
                self.process_message(msg)
            except socket.timeout:
                pass


class Server(object):
    def __init__(self, tcp_ip, tcp_port):
        self.tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.tcp_server.bind((tcp_ip, tcp_port))

        # Allow up to 4 connections
        self.tcp_server.listen(4)

        # Set for clients
        self.clients = set()

    def run(self):
        """ Run server"""
        while True:
            client_socket, client_address = self.tcp_server.accept()

            print ("{}:{} has connected.".format(
                client_address[0], client_address[1]
            ))

            user = Client(client_socket, self)

            Thread(target=user.start_working_loop).start()

    def broadcast(self, message, from_client=None):
        """ Send message to all connected users.
        :param str message: text of message
        :param Client from_client: Author of message. If None message will be
            send as SYSTEM
        """
        for client in self.clients:
            if from_client:
                # User msg
                client.client_socket.send(
                    '{} | {} : {} '.format(
                        get_now(),
                        from_client.name,
                        message
                    )
                )
            else:
                # System msg
                client.client_socket.send(
                    '{} | SYSTEM: {}'.format(
                        get_now(),
                        message
                    )
                )


if __name__ == '__main__':
    server = Server(TCP_IP, TCP_PORT)
    server.run()
