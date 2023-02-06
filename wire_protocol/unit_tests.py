import unittest
from memory_manager import User, MemoryManager
from client import get_alphanumeric_input
from server import *
from receiver_thread import ReceiverThread
from server_thread import ServerThread



class WireProtocolTestCase(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')




if __name__ == '__main__':
    unittest.main()