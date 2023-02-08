import grpc
from concurrent import futures
from . import chatbot_pb2
from . import chatbot_pb2_grpc
from helpers.memory_manager import MemoryManager


ServerMemory = MemoryManager()


class ChatBot(chatbot_pb2_grpc.ChatBotServicer):
    def __init__(self):
        # TODO  this is getting shared across threads, need to figure out thread specific memory
        self.logged_in_user = ""

    def create_user(self, request, _context):
        username = request.username
        print("CREATING USER", username)
        result = ServerMemory.create_user(username)
        response = "CREATE:SUCCESS:EOM" if result else "CREATE:FAILURE:EOM"
        return chatbot_pb2.ChatbotReply(message=response)

    def login_user(self, request, _context):
        username = request.username
        print("LOGGING IN USER", username)
        if username in ServerMemory.users:
            self.logged_in_user = username
            return chatbot_pb2.ChatbotReply(message='LOGIN:SUCCESS:EOM')
        else:
            return chatbot_pb2.ChatbotReply(message='LOGIN:FAILURE:EOM')

    def send_message(self, request, _context):
        to = request.username
        message = request.message
        print("SENDING MESSAGE", message, "TO", to)
        if self.logged_in_user != "":
            call_result = ServerMemory.send_message(
                self.logged_in_user, to, message)
            response = "SEND:SUCCESS:EOM" if call_result else "SEND:FAILURE:EOM"
            return chatbot_pb2.ChatbotReply(message=response)
        else:
            return chatbot_pb2.ChatbotReply(message='SEND:FAILURE:LOGIN_REQUIRED:EOM')

    def list_users(self, request, _context):
        wildcard = request.wildcard
        print("LISTING USERS", wildcard)
        matches = ", ".join(ServerMemory.list_users(wildcard))
        return_msg = "LIST:{}:EOM".format(matches)
        return chatbot_pb2.ChatbotReply(message=return_msg)

    def get_message(self, request, _context):
        if self.logged_in_user == "":
            return chatbot_pb2.ChatbotReply(message='')
        msg = ServerMemory.get_message(self.logged_in_user)
        if msg:
            return chatbot_pb2.ChatbotReply(message=f"{self.logged_in_user}:{msg}")
        else:
            return chatbot_pb2.ChatbotReply(message='')

    def delete_user(self, request, _context):
        username = request.username
        print("DELETING USER", username)
        if username != "":
            result = ServerMemory.delete_user(username)
            response = "DELETE:SUCCESS:EOM" if result else "DELETE:FAILURE:EOM"
            return chatbot_pb2.ChatbotReply(message=response)


def run_server():
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    chatbot_pb2_grpc.add_ChatBotServicer_to_server(ChatBot(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("GRPC Server started, listening on " + port)
    server.wait_for_termination()
