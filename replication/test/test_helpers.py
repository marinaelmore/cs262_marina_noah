import unittest
from grpc_chatbot.helpers.memory_manager import User, MemoryManager
from unittest.mock import patch, Mock, MagicMock, mock_open
from grpc_chatbot.grpc_client import *
from grpc_chatbot.grpc_server import *
import os

class MockThread:
    def __init__(self, socket):
        self.client_socket = socket
    
    def start(self):
        pass

    def send(self, msg):
        print("Sending: {}".format(msg))
        self.client_socket = msg

    def recv(self, msg):
        self.client_socket = None
        return b""


class MockSocket:
    def __init__(self) -> None:
        pass

    def send(self):
        print("Sending")
        pass 

    def recv(self, bytes):
        return ""

class mockedChatbotPb2:
    def __init__(self) -> None:
       self.logged_in_user = ""
       self.message = ""

    def ChatbotReply(self, message="", SET_LOGIN_USER=""):
        self.message = message
        self.logged_in_user = SET_LOGIN_USER

class MockedGRPCRequest:
    def __init__(self, username, logged_in_user="", message=""):
        self.username = username
        self.logged_in_user = logged_in_user
        self.message = message

class MockedChatbotReply:
    def __init__(self, message, SET_LOGIN_USER=""):
        self.message = message
        self.SET_LOGIN_USER = SET_LOGIN_USER

class MockedMessageRequest:
    def __init__(self, logged_in_user, username, message):
        self.logged_in_user = logged_in_user
        self.username = username
        self.message = message


class MockedListRequest:
    def __init__(self, wildcard):
        self.wildcard = wildcard

class TestUser(unittest.TestCase):

    def test_user_creation(self):
        user = User("Alice")
        self.assertEqual(user.username, "Alice")
        self.assertEqual(user.messages, [])

    def test_add_message(self):
        user = User("Bob")
        user.add_message("Hello")
        self.assertEqual(user.messages, ["Hello"])

    def test_user_to_dict(self):
        user = User("Charlie")
        user.add_message("Hello")
        self.assertEqual(user.user_to_dict(), {"Charlie": ["Hello"]})


class TestMemoryManager(unittest.TestCase):

    def setUp(self):
        self.primary = Mock()
        self.backup_servers = [Mock() for i in range(3)]
        self.filename = "test/test.json"

    @patch("grpc_chatbot.helpers.memory_manager.MemoryManager.persist_and_replicate")
    @patch("grpc_chatbot.helpers.memory_manager.MemoryManager.get_state_from_primary", return_value=False)
    @patch("builtins.open", mock_open(read_data='{"Alice": ["Hi"]}'))
    def test_initialize_memory_from_file(self, mock_get_state, mock_persist):
        manager = MemoryManager(self.primary, self.backup_servers, self.filename)
        self.assertTrue(mock_get_state.called)
        self.assertTrue(mock_persist.called)
        self.assertIn("Alice", manager.users)
        self.assertEqual(manager.users["Alice"].messages, ["Hi"])


    @patch("grpc_chatbot.helpers.memory_manager.MemoryManager.persist_and_replicate")
    @patch("grpc_chatbot.helpers.memory_manager.MemoryManager.get_state_from_primary", return_value=True)
    def test_sync_state_mismatch_hashes(self, mock_get_state, mock_persist):
        manager = MemoryManager(self.primary, self.backup_servers, self.filename)
        manager.sync_state("hash1", "hash2", '[{"op": "add", "path": "/Alice/0", "value": "Hello"}]')


if __name__ == '__main__':
    unittest.main()
