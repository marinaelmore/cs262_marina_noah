import unittest
from helpers.memory_manager import User, MemoryManager
from chatbot.receiver_thread import ReceiverThread
from chatbot.server_thread import ServerThread
from unittest.mock import patch
import select


class MockThread:
    def __init__(self, socket):
        self.client_socket = socket
    
    def start(self):
        pass

    def send(self, msg):
        print("Sending: {}".format(msg))
        self.client_socket = msg


class MockSocket:
    def __init__(self) -> None:
        pass

    def send(self):
        print("Sending")
        pass 


class WireProtocolTestCase(unittest.TestCase):

    def setUp(self):
        self.username = "narina"
        self.username1 = "moah"
        self.message = "hello from the other side"
        self.user = User(self.username)
        self.memory_manager = MemoryManager()

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


    def test_Chatbot_server_thread(self):

        with patch('helpers.memory_manager.MemoryManager') as memory_mock:
            mocked_socket = MockSocket()
            mocked_thread = MockThread(mocked_socket)
            server_thread = ServerThread(mocked_thread)
            
            # Create
            self.assertEqual(None, server_thread.create(self.username))

            # Login
            server_thread.login(self.username)     
            self.assertEqual(server_thread.logged_in_user, self.username)

            # Send to non-logged in user
            server_thread.send(self.username1, self.message)
            self.assertEqual(mocked_thread.client_socket,b"SEND:FAILURE:EOM")

            server_thread2 = ServerThread(mocked_thread)
            server_thread2.create(self.username1)
            server_thread2.login(self.username1)     
            self.assertEqual(server_thread2.logged_in_user, self.username1)
            
            # Send to logged in user
            server_thread.send(self.username1, self.message)
            self.assertEqual(mocked_thread.client_socket,b"SEND:SUCCESS:EOM")

            # List Users


        
        self.assertEqual("marina", "marina")


    
    def test_Chatbot_grpc(self):
        self.assertEqual("marina", "marina")


if __name__ == '__main__':
    unittest.main()
