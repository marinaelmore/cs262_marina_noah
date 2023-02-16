import unittest
from helpers.memory_manager import User, MemoryManager
from chatbot.receiver_thread import ReceiverThread
from chatbot.server_thread import ServerThread
from unittest.mock import patch, Mock, MagicMock
from grpc_chatbot.grpc_server import ChatBot

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
        server_thread.list_users("")
        list_string = "LIST:{}, {}:EOM".format(self.username, self.username1) 
        self.assertEqual(mocked_thread.client_socket,list_string.encode())

        # Delete User           
        server_thread.delete(self.username)
        delete_string = "DELETE:SUCCESS:EOM"
        self.assertEqual(mocked_thread.client_socket,delete_string.encode())


    def test_Chatbot_grpc_server(self):
        mocked_chatbot_reply = MagicMock()

        with patch('grpc_chatbot.chatbot_pb2') as mock_chatbot_reply:
            mock_chatbot_reply.ChatbotReply.return_value = MockedChatbotReply(SET_LOGIN_USER="", message=mock_chatbot_reply.message)
            grpc_server_thread = ChatBot()

            # Create User
            user_request = MockedGRPCRequest(username=self.username)
            self.assertEqual("CREATE:SUCCESS:EOM", grpc_server_thread.create_user(user_request,"").message)

            # Login User
            user_request_exists = MockedGRPCRequest(username=self.username)
            user_request_dn_exist = MockedGRPCRequest(username=self.username1)

            logged_in_reply = grpc_server_thread.login_user(user_request_exists, "")
            self.assertEqual("LOGIN:SUCCESS:EOM", logged_in_reply.message)
            self.assertEqual(self.username, logged_in_reply.SET_LOGIN_USER)

            self.assertEqual("LOGIN:FAILURE:EOM", grpc_server_thread.login_user(user_request_dn_exist, "").message)


            # Send Message
            ## Send to non-logged in user
            message_request = MockedMessageRequest(logged_in_user=self.username, username=self.username1, message=self.message)
            self.assertEqual("SEND:FAILURE:EOM", grpc_server_thread.send_message(message_request, "").message)

            # Create Second User
            user_request1 = MockedGRPCRequest(username=self.username1)
            self.assertEqual("CREATE:SUCCESS:EOM", grpc_server_thread.create_user(user_request1,"").message)

            # Message Failure - Not Logged In
            message_request = MockedMessageRequest(logged_in_user="", username=self.username1, message=self.message)
            self.assertEqual("SEND:FAILURE:LOGIN_REQUIRED:EOM", grpc_server_thread.send_message(message_request, "").message)

            # Login Second User
            logged_in_reply = grpc_server_thread.login_user(user_request_dn_exist, "")
            self.assertEqual("LOGIN:SUCCESS:EOM", logged_in_reply.message)
            self.assertEqual(self.username1, logged_in_reply.SET_LOGIN_USER)

            # Send Message to User
            message_request = MockedMessageRequest(logged_in_user=logged_in_reply.SET_LOGIN_USER, username=self.username1, message=self.message)
            self.assertEqual("SEND:SUCCESS:EOM", grpc_server_thread.send_message(message_request, "").message)

            # List Users
            list_request = MockedListRequest(wildcard="")
            self.assertEqual("LIST:{}, {}:EOM".format(self.username, self.username1), grpc_server_thread.list_users(list_request, "").message)

            # Delete User
            delete_request = MockedGRPCRequest(username=self.username)
            self.assertEqual("DELETE:SUCCESS:EOM", grpc_server_thread.delete_user(delete_request, "").message)
            self.assertEqual("LIST:{}:EOM".format(self.username1), grpc_server_thread.list_users(list_request, "").message)


if __name__ == '__main__':
    unittest.main()
