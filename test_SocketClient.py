import unittest
from unittest.mock import Mock
from unittest.mock import patch
import socket
from SocketClient import SocketClient

class SocketClientTestCase(unittest.TestCase):

    def test_create_connect_destroy(self):
        with patch('socket.socket') as socket_mock:
            mock = Mock()
            socket_mock.return_value = mock

            sC = SocketClient()
            del sC

            socket_mock.assert_called_with(socket.AF_INET, socket.SOCK_STREAM)
            mock.connect.assert_called_with(("127.0.0.1", 5001))
            mock.close.assert_called()

    def test_server_params(self):
        with patch('socket.socket') as socket_mock:
            mock = Mock()
            socket_mock.return_value = mock

            sC = SocketClient("1.2.3.4", 1234)
            del sC

            socket_mock.assert_called_with(socket.AF_INET, socket.SOCK_STREAM)
            mock.connect.assert_called_with(("1.2.3.4", 1234))

    def test_sending(self):
        with patch('socket.socket') as socket_mock:
            mock = Mock()
            socket_mock.return_value = mock

            sC = SocketClient()
            sC.Send("ABBA")
            del sC

            mock.send.assert_called_with(b"ABBA")

    def test_receive(self):
        with patch('socket.socket') as socket_socket_mock:
            with patch('select.select') as select_select_mock:
                socket_obj_mock = Mock()
                socket_obj_mock.recv.return_value = b"ABCD"
                socket_socket_mock.return_value = socket_obj_mock

                select_select_mock.return_value = ([socket_obj_mock],[],[])
                
                sC = SocketClient()
                data = sC.Receive(1.5)
                del sC

                select_select_mock.assert_called_with([socket_obj_mock],[],[],1.5)
                socket_obj_mock.recv.assert_called_with(1024)
                assert data == b"ABCD"
                
    def test_receive_nothing_to_receive(self):
        with patch('socket.socket') as socket_socket_mock:
            with patch('select.select') as select_select_mock:
                socket_obj_mock = Mock()
                socket_socket_mock.return_value = socket_obj_mock

                select_select_mock.return_value = ([],[],[])
                
                sC = SocketClient()
                data = sC.Receive(1.5)
                del sC

                select_select_mock.assert_called_with([socket_obj_mock],[],[],1.5)
                assert not socket_obj_mock.recv.called
                assert data == ""

if __name__ == '__main__':
    unittest.main()