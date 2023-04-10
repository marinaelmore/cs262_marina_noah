import unittest
import grpc
import json
from concurrent import futures
from grpc_chatbot.grpc_server import ChatBotServer
from grpc_chatbot.proto_files.chatbot_pb2_grpc import add_ChatBotServicer_to_server
from grpc_chatbot.proto_files.chatbot_pb2_grpc import ChatBotStub
from grpc_chatbot.proto_files.chatbot_pb2 import UserRequest, ChatbotReply, MessageRequest, ListRequest
from mock import patch
import threading

class TestChatBotServer(unittest.TestCase):

    #@patch('grpc_chatbot.helpers.heartbeat_thread.HeartbeatThread')
    #@patch('threading.Thread')
    def setUp(self):
        self.server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        add_ChatBotServicer_to_server(ChatBotServer('test.json', 1), self.server)
        self.server.add_insecure_port('[::]:50051')
        self.server.start()
        self.client = ChatBotStub(grpc.insecure_channel('localhost:50051'))

    def tearDown(self):
        self.server.stop(None)


        #for thread in all_child_threads:
        #    thread.daemon = True

    def test_create_user(self):
        response = self.client.create_user(UserRequest(username='user1'))
        self.assertEqual(response.message, 'Failure to create user: user1.')

    def test_login_user(self):
        self.client.create_user(UserRequest(username='user2'))
        response = self.client.login_user(UserRequest(username='user2'))
        self.assertEqual(response.SET_LOGIN_USER, 'user2')

    def test_send_message(self):
        self.client.create_user(UserRequest(username='user3'))
        self.client.create_user(UserRequest(username='user4'))
        self.client.login_user(UserRequest(username='user3'))
        response = self.client.send_message(MessageRequest(logged_in_user='user3', username='user4', message='hello'))
        self.assertEqual(response.message, 'Messaged successfully sent.')

    def test_list_users(self):
        self.client.create_user(UserRequest(username='user5'))
        self.client.create_user(UserRequest(username='user6'))
        response = self.client.list_users(ListRequest(wildcard=''))
        self.assertEqual(response.message, 'Current users: user1, user2, user3, user4, user5, user6, user7, user8')

    def test_get_message(self):
        self.client.create_user(UserRequest(username='user7'))
        self.client.create_user(UserRequest(username='user8'))
        self.client.login_user(UserRequest(username='user8'))
        self.client.send_message(MessageRequest(logged_in_user='user8', username='user7', message='hello'))
        response = self.client.get_message(MessageRequest(logged_in_user='user7'))
        self.assertEqual(response.message, '{}: hello'.format("user8"))

if __name__ == '__main__':
    unittest.main()

    all_child_threads = [thread for thread in threading.enumerate() if thread != threading.main_thread()]
    for child_thread in all_child_threads:
        child_thread.join()