import unittest
from unittest.mock import Mock
from unittest.mock import patch
from GaduGaduClient import GaduGaduClient

class GaduGaduClientTestCase(unittest.TestCase):

    def test_create(self):
        mock = Mock()

        client = GaduGaduClient(mock)
        assert client.socketClient == mock
        del client

        assert not mock.called

    def test_login(self):
        mock = Mock()
        client = GaduGaduClient(mock)
        client.Login("Karol")
        del client

        mock.Send.assert_called_with("LOGIN:Karol")
        
    def test_send_msg(self):
        mock = Mock()
        client = GaduGaduClient(mock)
        client.SendMsg("user1:czesc")
        del client

        mock.Send.assert_called_with("MSG_TO:user1:czesc")

if __name__ == '__main__':
    unittest.main()