import unittest
from unittest.mock import Mock
from unittest.mock import patch
from unittest.mock import call
from GaduGaduServer import GaduGaduServer

class GaduGaduServerTestCase(unittest.TestCase):

    def test_create(self):
        mock = Mock()

        server = GaduGaduServer(mock)
        assert server.socketServer == mock
        del server

        assert not mock.called

    def test_process_not_valid_data(self):
        socketMock = Mock()
        mock = Mock()
        mock.CheckForMsg.return_value = [(socketMock, "TestData")]
        server = GaduGaduServer(mock)
        server.Process()
        del server

        mock.CheckForMsg.assert_called_with()
        assert not mock.SendTo.called

    def test_process_empty(self):
        mock = Mock()
        mock.CheckForMsg.return_value = []
        server = GaduGaduServer(mock)
        server.Process()
        del server

        mock.CheckForMsg.assert_called_with()
        assert not mock.SendTo.called

    def test_login_first_user(self):
        socketMock = Mock()
        mock = Mock()
        mock.CheckForMsg.return_value = [(socketMock,"LOGIN:user1")]
        server = GaduGaduServer(mock)
        server.Process()
        del server

        mock.CheckForMsg.assert_called_with()
        mock.SendTo.assert_called_with(socketMock,"USERS:user1")


    def test_login_two_user(self):
        socketMock1 = Mock()
        socketMock2 = Mock()
        mock = Mock()
        mock.CheckForMsg.return_value = [(socketMock1,"LOGIN:user1"),(socketMock2,"LOGIN:user2")]
        server = GaduGaduServer(mock)
        server.Process()
        del server

        mock.CheckForMsg.assert_called_with()
        mock.SendTo.assert_has_calls([call(socketMock1,"USERS:user1"), call(socketMock1,"USERS:user1,user2"),call(socketMock2,"USERS:user1,user2")])
        
    def test_msg_from_client(self):
        socketMockSender = Mock()
        socketMockReceiver = Mock()
        mock = Mock()
        mock.CheckForMsg.return_value = [(socketMockSender,"MSG_TO:user1:czesc")]
        server = GaduGaduServer(mock)
        server.users_list = [(socketMockSender,"nick"),(socketMockReceiver,"user1")]
        server.Process()
        del server

        mock.CheckForMsg.assert_called_with()
        mock.SendTo.assert_called_with(socketMockReceiver,"MSG_FROM:nick:czesc")

    def test_msg_from_client_wrong_destination(self):
        socketMockSender = Mock()
        socketMockReceiver = Mock()
        mock = Mock()
        mock.CheckForMsg.return_value = [(socketMockSender,"MSG_TO:user1:czesc")]
        server = GaduGaduServer(mock)
        server.users_list = [(socketMockSender,"nick"),(socketMockReceiver,"user2")]
        server.Process()
        del server

        mock.CheckForMsg.assert_called_with()
        assert not socketMockReceiver.SendTo.called
        mock.SendTo.assert_called_with(socketMockSender,"MSG_ERROR:user1 not logged")

    def test_client_error(self):
        socketMockSender = Mock()
        socketMockReceiver = Mock()
        socketMockReceiver2 = Mock()
        mock = Mock()
        mock.CheckForMsg.return_value = [(socketMockSender,"ERROR")]
        server = GaduGaduServer(mock)
        server.users_list = [(socketMockSender,"nick"),(socketMockReceiver,"user1"),(socketMockReceiver2,"user2")]
        server.Process()
        assert server.users_list == [(socketMockReceiver,"user1"),(socketMockReceiver2,"user2")]
        del server

        mock.CheckForMsg.assert_called_with()
        mock.SendTo.assert_has_calls([call(socketMockReceiver,"USERS:user1,user2")])

    def test_client_disconnect(self):
        socketMockSender = Mock()
        socketMockReceiver = Mock()
        socketMockReceiver2 = Mock()
        mock = Mock()
        mock.CheckForMsg.return_value = [(socketMockSender,"DISCONNECT")]
        server = GaduGaduServer(mock)
        server.users_list = [(socketMockSender,"nick"),(socketMockReceiver,"user1"),(socketMockReceiver2,"user2")]
        server.Process()
        assert server.users_list == [(socketMockReceiver,"user1"),(socketMockReceiver2,"user2")]
        del server

        mock.CheckForMsg.assert_called_with()
        mock.SendTo.assert_has_calls([call(socketMockReceiver,"USERS:user1,user2")])

if __name__ == '__main__':
    unittest.main()