import unittest
from unittest.mock import Mock
from unittest.mock import patch
import socket
from SocketServer import SocketServer

class SocketServerTestCase(unittest.TestCase):

    def test_create_listen_destroy(self):
        with patch('socket.socket') as socket_mock:
            mock = Mock()
            socket_mock.return_value = mock

            sS = SocketServer()
            del sS

            socket_mock.assert_called_with(socket.AF_INET, socket.SOCK_STREAM, socket.getprotobyname('TCP'))
            mock.bind.assert_called_with(("0.0.0.0", 5001))
            mock.listen.assert_called()
            mock.close.assert_called()

    def test_server_params(self):
        with patch('socket.socket') as socket_mock:
            mock = Mock()
            socket_mock.return_value = mock

            sS = SocketServer("1.2.3.4", 1234)
            del sS

            socket_mock.assert_called_with(socket.AF_INET, socket.SOCK_STREAM, socket.getprotobyname('TCP'))
            mock.bind.assert_called_with(("1.2.3.4", 1234))

    def test_check_for_new_clients(self):
        with patch('socket.socket') as socket_socket_mock:
            with patch('select.select') as select_select_mock:

                serverSocketMock = Mock()
                clientSocketMock = Mock()
                socket_socket_mock.return_value = serverSocketMock
                select_select_mock.return_value = ([serverSocketMock],[],[])
                serverSocketMock.accept.return_value = (clientSocketMock, ("1.2.3.4", 1234))
                
                sS = SocketServer("1.2.3.4", 1234)
                sS.CheckForNewClient(1.5)
                assert sS.clientSocketList == [clientSocketMock]
                del sS
                
                select_select_mock.assert_called_with([serverSocketMock],[],[],1.5)
                serverSocketMock.accept.assert_called()

    def test_check_for_new_clients_no_clients(self):
        with patch('socket.socket') as socket_socket_mock:
            with patch('select.select') as select_select_mock:

                serverSocketMock = Mock()
                socket_socket_mock.return_value = serverSocketMock
                select_select_mock.return_value = ([],[],[])
                
                sS = SocketServer("1.2.3.4", 1234)
                sS.CheckForNewClient(1.5)
                assert sS.clientSocketList == []
                del sS
                
                select_select_mock.assert_called_with([serverSocketMock],[],[],1.5)
                assert not serverSocketMock.accept.called


    def test_check_for_msg_no_clients(self):
        with patch('socket.socket') as socket_socket_mock:
            with patch('select.select') as select_select_mock:
                serverSocketMock = Mock()
                socket_socket_mock.return_value = serverSocketMock

                
                sS = SocketServer("1.2.3.4", 1234)
                assert sS.clientSocketList == []
                assert [] == sS.CheckForMsg(1.5)
                assert sS.clientSocketList == []
                del sS
                
                assert not select_select_mock.called
                
    def test_check_for_msg_single_client(self):
        with patch('socket.socket') as socket_socket_mock:
            with patch('select.select') as select_select_mock:
                serverSocketMock = Mock()
                socket_socket_mock.return_value = serverSocketMock
                socketClientMock = Mock()
                socketClientMock.recv.return_value = b"ABCD"
                select_select_mock.return_value = ([socketClientMock],[],[])
                
                sS = SocketServer("1.2.3.4", 1234)
                sS.clientSocketList = [socketClientMock]
                assert [(socketClientMock,"ABCD")] == sS.CheckForMsg()
                del sS

                select_select_mock.assert_called_with([socketClientMock],[],[],0.2)
                socketClientMock.recv.assert_called_with(1024)
                
    def test_check_for_msg_many_client(self):
        with patch('socket.socket') as socket_socket_mock:
            with patch('select.select') as select_select_mock:
                serverSocketMock = Mock()
                socket_socket_mock.return_value = serverSocketMock
                socketClientMock1 = Mock()
                socketClientMock1.recv.return_value = b"ABCD"
                socketClientMock2 = Mock()
                select_select_mock.return_value = ([socketClientMock1],[],[])
                
                sS = SocketServer("1.2.3.4", 1234)
                sS.clientSocketList = [socketClientMock1, socketClientMock2]
                assert [(socketClientMock1,"ABCD")] == sS.CheckForMsg()
                del sS

                select_select_mock.assert_called_with([socketClientMock1, socketClientMock2],[],[],0.2)
                socketClientMock1.recv.assert_called_with(1024)

    def test_send_to(self):
        with patch('socket.socket') as socket_mock:
            mock = Mock()
            socket_mock.return_value = mock
            clientMock = Mock()

            sS = SocketServer("1.2.3.4", 1234)
            sS.SendTo(clientMock, "DATA");
            del sS

            socket_mock.assert_called_with(socket.AF_INET, socket.SOCK_STREAM, socket.getprotobyname('TCP'))
            mock.bind.assert_called_with(("1.2.3.4", 1234))
            clientMock.send.assert_called_with(b"DATA")

    def test_check_for_msg_client_with_error(self):
        with patch('socket.socket') as socket_socket_mock:
            with patch('select.select') as select_select_mock:
                serverSocketMock = Mock()
                socket_socket_mock.return_value = serverSocketMock
                socketClientMock = Mock()
                socketClientMock.recv.return_value = b"ABCD"
                socketClientMock.recv.side_effect = socket.error
                select_select_mock.return_value = ([socketClientMock],[],[])

                sS = SocketServer("1.2.3.4", 1234)
                sS.clientSocketList = [socketClientMock]
                assert [(socketClientMock,"ERROR")] == sS.CheckForMsg()
                socketClientMock.recv.assert_called_with(1024)
                assert socketClientMock.close.called
                assert sS.clientSocketList == []
                del sS

if __name__ == '__main__':
    unittest.main()