import grpc
from concurrent import futures
from . import chatbot_pb2
from . import chatbot_pb2_grpc
from helpers.memory_manager import MemoryManager

# Start shared memory manager for server
ServerMemory = MemoryManager()


class ChatBot(chatbot_pb2_grpc.ChatBotServicer):

    # helper method to create a new user
    def create_user(self, request, _context):
        username = request.username
        print("CREATING USER", username)
        result = ServerMemory.create_user(username)
        response = "CREATE:SUCCESS:EOM" if result else "CREATE:FAILURE:EOM"
        return chatbot_pb2.ChatbotReply(message=response)

    # helper method to login a new user by setting the SET_LOGIN_USER header
    def login_user(self, request, _context):
        username = request.username
        print("LOGGING IN USER", username)
        if username in ServerMemory.users:
            return chatbot_pb2.ChatbotReply(SET_LOGIN_USER=username, message='LOGIN:SUCCESS:EOM')
        else:
            return chatbot_pb2.ChatbotReply(message='LOGIN:FAILURE:EOM')

    # send message from one logged in user to another
    def send_message(self, request, _context):
        logged_in_user = request.logged_in_user
        to = request.username
        message = request.message
        print("SENDING MESSAGE", message, "TO", to)
        if logged_in_user != "":
            call_result = ServerMemory.send_message(
                logged_in_user, to, message)
            response = "SEND:SUCCESS:EOM" if call_result else "SEND:FAILURE:EOM"
            return chatbot_pb2.ChatbotReply(message=response)
        else:
            return chatbot_pb2.ChatbotReply(message='SEND:FAILURE:LOGIN_REQUIRED:EOM')

# list users matching with a wildcard
    def list_users(self, request, _context):
        wildcard = request.wildcard
        print("LISTING USERS", wildcard)
        matches = ", ".join(ServerMemory.list_users(wildcard))
        return_msg = "LIST:{}:EOM".format(matches)
        return chatbot_pb2.ChatbotReply(message=return_msg)

# read a message that has been sent to the logged in user
    def get_message(self, request, _context):
        logged_in_user = request.logged_in_user
        if logged_in_user == "":
            return chatbot_pb2.ChatbotReply(message='')
        msg = ServerMemory.get_message(logged_in_user)
        if msg:
            return chatbot_pb2.ChatbotReply(message=msg)
        else:
            return chatbot_pb2.ChatbotReply(message='')

# delete user
    def delete_user(self, request, _context):
        username = request.username
        print("DELETING USER", username)
        if username != "":
            result = ServerMemory.delete_user(username)
            response = "DELETE:SUCCESS:EOM" if result else "DELETE:FAILURE:EOM"
            return chatbot_pb2.ChatbotReply(message=response)

# main server function


def run_server():
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    chatbot_pb2_grpc.add_ChatBotServicer_to_server(ChatBot(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("GRPC Server started, listening on " + port)
    server.wait_for_termination()
