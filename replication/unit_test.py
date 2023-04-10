import unittest
from grpc_chatbot.helpers.memory_manager import User, MemoryManager
from unittest.mock import patch, Mock, MagicMock


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

class WireProtocolTestCase(unittest.TestCase):

    def setUp(self):
        self.username = "narina"
        self.username1 = "moah"
        self.message = "hello from the other side"
        self.user = User(self.username)
        self.memory_manager = MemoryManager(False,[],"test.json")

    # Memory Manager - User Class
    def test_User_class(self):

        # Test creation
        self.assertEqual(self.user.username, self.username)
        self.assertEqual([], self.user.messages)

        # Test add message
        msg_list = []
        msg_list.append(self.message)
        self.user.add_message(self.message)
        self.assertEqual(msg_list, self.user.messages)


    def test_MemoryManager_class(self):

        # Test Creation
        self.assertEqual({}, self.memory_manager.users)

        # Test Create User
        self.memory_manager.create_user(self.username)
        self.memory_manager.create_user(self.username1)
        self.assertEqual(2, len(self.memory_manager.users))
        created_users = list(self.memory_manager.users.keys())
        self.assertEqual(["narina", "moah"], created_users)

        # Test Send Message (narina -> moah)
        self.memory_manager.send_message(self.username, self.username1, self.message)
        moahs_messages = self.memory_manager.users.get(self.username1).messages
        self.assertEqual(1, len(moahs_messages))
        message_format = "{}: {}".format(self.username, self.message)
        self.assertEqual(message_format, moahs_messages[0])

        # Test Get Message
        self.assertEqual(
            message_format, self.memory_manager.get_message(self.username1))
        self.assertIsNone(self.memory_manager.get_message(self.username))

        # Test List Users
        self.assertEqual(["narina", "moah"],
                         self.memory_manager.list_users(""))
        self.assertEqual(["narina"], self.memory_manager.list_users("n"))
        self.assertEqual(["moah"], self.memory_manager.list_users("m"))
        self.assertEqual([], self.memory_manager.list_users("9"))

        # Test Delete User
        self.assertEqual(2, len(self.memory_manager.users))
        self.memory_manager.delete_user(self.username)
        self.assertEqual(1, len(self.memory_manager.users))
        curr_users = list(self.memory_manager.users.keys())
        self.assertEqual(["moah"], curr_users)



if __name__ == '__main__':
    unittest.main()
