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

if __name__ == '__main__':
    unittest.main()