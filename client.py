# Python TCP Client A
#ala widzisz mnie ?
#ale jaja XDD widzę!
# to git


import socket
from threading import Thread
import os
from datetime import datetime
import sys

HOST = socket.gethostname()
PORT = 2004
BUFFER_SIZE = 2000

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


def get_now():
    return datetime.now().strftime(DATETIME_FORMAT)


class Client(object):

    def __init__(self, host, port):
        """ Initialize client.
        :param host: hostname
        :param port: port number """

        # Stop to stop threads
        self.stop = False

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.settimeout(1)

        try:
            self.client_socket.connect((host, port))
            self.start_working_loop()
        except socket.error:
            print ('Server is not working')
            return

    def send_message(self, message):
        """ Sends message to server.
        :param str message: text of message
        """

        self.client_socket.send(message.encode('utf-8'))

    def receive_message(self):
        """ Receives message from socket.
        :return message: text of message
        """
        message = self.client_socket.recv(BUFFER_SIZE).decode("utf-8")
        print (message)
        return message

    def wait_for_message(self):
        """ Method should be started via thread. Waiting for message."""
        while not self.stop:
            try:
                self.receive_message()
            except socket.timeout:
                pass

    def start_working_loop(self):
        """ Main working loop"""
        # Initialize tread to receive message
        Thread(target=self.wait_for_message).start()

        # Initialize event loop to send message
        try:
            while True:
                message = raw_input()
                if message == 'EXIT':
                    break

                self.send_message(message)
        finally:
            self.stop_working_loop()

    def stop_working_loop(self):
        self.client_socket.close()
        self.stop = True


if __name__ == '__main__':
    client = Client(HOST, PORT)

