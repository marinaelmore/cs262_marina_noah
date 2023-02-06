import unittest
from memory_manager import User, MemoryManager
#from client import get_alphanumeric_input
#from server import *
from receiver_thread import ReceiverThread
from server_thread import ServerThread


class WireProtocolTestCase(unittest.TestCase):

    def setUp(self):
        self.username = "marina"
        self.username1 = "noah"
        self.message = "hello from the other side"
        self.user = User(self.username)
        self.memory_manager = MemoryManager()

    #Memory Manager - User Class
    def test_User_class(self):
        
        #Test creation
        self.assertEqual(self.user.username, self.username)
        self.assertEqual([], self.user.messages)

        # Test add message
        msg_list = []
        msg_list.append(self.message)
        self.user.add_message(self.message)
        self.assertEqual(msg_list, self.user.messages)


    def test_MemoryManager_class(self):
        
        #Test Creation
        self.assertEqual({},self.memory_manager.users)

        # Test Create User
        self.memory_manager.create_user(self.username)
        self.memory_manager.create_user(self.username1)
        self.assertEqual(2, len(self.memory_manager.users))
        created_users = list(self.memory_manager.users.keys())
        self.assertEqual(["marina", "noah"], created_users)

        # Test Send Message (marina -> noah)
        self.memory_manager.send_message(self.username1, self.message)
        noahs_messages = self.memory_manager.users.get(self.username1).messages
        self.assertEqual(1, len(noahs_messages))
        self.assertEqual(self.message, noahs_messages[0])

        #Test Get Message
        self.assertEqual(self.message, self.memory_manager.get_message(self.username1))
        self.assertIsNone(self.memory_manager.get_message(self.username))

        #Test List Users
        self.assertEqual(["marina", "noah"], self.memory_manager.list_users(""))
        self.assertEqual(["marina"], self.memory_manager.list_users("m"))
        self.assertEqual(["noah"], self.memory_manager.list_users("n"))
        self.assertEqual([], self.memory_manager.list_users("9"))

        # Test Delete User
        self.assertEqual(2, len(self.memory_manager.users))
        self.memory_manager.delete_user(self.username)
        self.assertEqual(1, len(self.memory_manager.users))
        curr_users = list(self.memory_manager.users.keys())
        self.assertEqual(["noah"], curr_users)





if __name__ == '__main__':
    unittest.main()