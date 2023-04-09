import grpc
import json
from concurrent import futures
from .proto_files import chatbot_pb2
from .proto_files import chatbot_pb2_grpc
from .helpers.memory_manager import MemoryManager

# Start shared memory manager for server
ServerMemory = MemoryManager()


class ChatBotServer(chatbot_pb2_grpc.ChatBotServicer):

    def __init__(self, primary, filename):
        self.primary = primary
        if self.primary:
            ServerMemory.initialize_memory(filename)

        # connect to other servers as clients
        self.backup_servers = []
        # open servers.json and read in the list of servers
        with open('servers.json', 'r') as servers_file:
            # load json
            server_json = json.loads(servers_file.read())
            # iterate through servers and add them to the backup_servers list
            for server in server_json['servers']:
                self.backup_servers.append(grpc.insecure_channel(
                    f"{server['host']}:{server['port']}"))

    def create_user(self, request, _context):
        username = request.username
        print("CREATING USER", username)
        result = ServerMemory.create_user(username)
        response = "Successfully created user: {}.".format(
            username) if result else "Failure to create user: {}.".format(username)
        return chatbot_pb2.ChatbotReply(message=response)

    # helper method to login a new user by setting the SET_LOGIN_USER header
    def login_user(self, request, _context):
        username = request.username
        print("LOGGING IN USER", username)
        if username in ServerMemory.users:
            return chatbot_pb2.ChatbotReply(SET_LOGIN_USER=username, message='Sucessfully logged in user: {}.'.format(username))
        else:
            return chatbot_pb2.ChatbotReply(message='Failed to login user: {}'.format(username))

    # send message from one logged in user to another
    def send_message(self, request, _context):
        logged_in_user = request.logged_in_user
        to = request.username
        message = request.message
        print("SENDING MESSAGE", message, "TO", to)
        if logged_in_user != "":
            call_result = ServerMemory.send_message(
                logged_in_user, to, message)
            response = "Messaged successfully sent." if call_result else "Failure to send message."
            return chatbot_pb2.ChatbotReply(message=response)
        else:
            return chatbot_pb2.ChatbotReply(message='Failure - please login to send a message.'.format(request.username))


# list users matching with a wildcard

    def list_users(self, request, _context):
        wildcard = request.wildcard
        print("LISTING USERS", wildcard)
        matches = ", ".join(ServerMemory.list_users(wildcard))
        return_msg = "Current users: {}".format(matches)
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
            response = "Successfully deleted user {}.".format(
                username) if result else "Failed to delete user {}".format(username)
            return chatbot_pb2.ChatbotReply(message=response)

# main server function


def run_server(primary, filename, port):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    chatbot_pb2_grpc.add_ChatBotServicer_to_server(
        ChatBotServer(primary, filename), server)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print("GRPC Server started, listening on ",  port)
    server.wait_for_termination()
