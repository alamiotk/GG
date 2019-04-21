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

    def test_process_data(self):
        mock = Mock()
        mock.CheckForMsg.return_value = ["TestData"]
        server = GaduGaduServer(mock)
        server.Process()
        del server

        mock.CheckForMsg.assert_called_with()
        mock.SendToAll.assert_called_with("TestData")

    def test_process_empty(self):
        mock = Mock()
        mock.CheckForMsg.return_value = []
        server = GaduGaduServer(mock)
        server.Process()
        del server

        mock.CheckForMsg.assert_called_with()
        assert not mock.SendToAll.called

    def test_login_first_user(self):
        mock = Mock()
        mock.CheckForMsg.return_value = ["LOGIN:user1"]
        server = GaduGaduServer(mock)
        server.Process()
        del server

        mock.CheckForMsg.assert_called_with()
        mock.SendToAll.assert_called_with("USERS:user1")


    def test_login_two_user(self):
        mock = Mock()
        mock.CheckForMsg.return_value = ["LOGIN:user1","LOGIN:user2"]
        server = GaduGaduServer(mock)
        server.Process()
        del server

        mock.CheckForMsg.assert_called_with()
        mock.SendToAll.assert_has_calls([call("USERS:user1"), call("USERS:user1,user2")])
        
if __name__ == '__main__':
    unittest.main()