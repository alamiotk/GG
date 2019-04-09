import unittest
from unittest.mock import Mock
from unittest.mock import patch
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


if __name__ == '__main__':
    unittest.main()