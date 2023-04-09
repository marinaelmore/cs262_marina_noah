import grpc
import json
from concurrent import futures
from .proto_files import chatbot_pb2
from .proto_files import chatbot_pb2_grpc
from .helpers.memory_manager import MemoryManager
from .helpers.heartbeat_thread import HeartbeatThread


class ChatBotServer(chatbot_pb2_grpc.ChatBotServicer):
    def __init__(self, primary, filename, server_id):
        self.primary = primary
        self.filename = filename

        # connect to other servers as clients
        self.backup_servers = []
        # open servers.json and read in the list of servers
        with open('servers.json', 'r') as servers_file:
            # load json
            server_json = json.loads(servers_file.read())
            # iterate through servers and add them to the backup_servers list
            for server in server_json['servers']:
                if server['global_id'] == server_id:
                    continue
                channel = grpc.insecure_channel(
                    f"{server['host']}:{server['port']}")
                client = chatbot_pb2_grpc.ChatBotStub(channel)
                self.backup_servers.append(client)

        # Start shared memory manager for server
        self.ServerMemory = MemoryManager(
            self.primary, self.backup_servers, self.filename)
        if self.primary:
            self.ServerMemory.initialize_memory()

        HeartbeatThread(self.backup_servers, server_id)

    def create_user(self, request, _context):
        username = request.username
        print("CREATING USER", username)
        result = self.ServerMemory.create_user(username)
        response = "Successfully created user: {}.".format(
            username) if result else "Failure to create user: {}.".format(username)
        return chatbot_pb2.ChatbotReply(message=response)

    # helper method to login a new user by setting the SET_LOGIN_USER header
    def login_user(self, request, _context):
        username = request.username
        print("LOGGING IN USER", username)
        if username in self.ServerMemory.users:
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
            call_result = self.ServerMemory.send_message(
                logged_in_user, to, message)
            response = "Messaged successfully sent." if call_result else "Failure to send message."
            return chatbot_pb2.ChatbotReply(message=response)
        else:
            return chatbot_pb2.ChatbotReply(message='Failure - please login to send a message.'.format(request.username))

    def sync_state(self, request, _context):
        print("SYNCING STATE")
        self.ServerMemory.sync_state(
            request.from_hash, request.to_hash, request.diff)
        return chatbot_pb2.Empty()

    def get_full_state(self, _request, _context):
        print("GET FULL STATE")
        state = json.dumps(self.ServerMemory.memory_to_dict(), sort_keys=True)
        print("sending state", state)
        return chatbot_pb2.FullStateReply(state=state)


# list users matching with a wildcard

    def list_users(self, request, _context):
        wildcard = request.wildcard
        print("LISTING USERS", wildcard)
        matches = ", ".join(self.ServerMemory.list_users(wildcard))
        return_msg = "Current users: {}".format(matches)
        return chatbot_pb2.ChatbotReply(message=return_msg)

# read a message that has been sent to the logged in user
    def get_message(self, request, _context):
        logged_in_user = request.logged_in_user
        if logged_in_user == "":
            return chatbot_pb2.ChatbotReply(message='')
        msg = self.ServerMemory.get_message(logged_in_user)
        if msg:
            return chatbot_pb2.ChatbotReply(message=msg)
        else:
            return chatbot_pb2.ChatbotReply(message='')

# delete user
    def delete_user(self, request, _context):
        username = request.username
        print("DELETING USER", username)
        if username != "":
            result = self.ServerMemory.delete_user(username)
            response = "Successfully deleted user {}.".format(
                username) if result else "Failed to delete user {}".format(username)
            return chatbot_pb2.ChatbotReply(message=response)

    def heartbeat(self, request, _context):
        print("HEARTBEAT")
        print(request)
        return chatbot_pb2.Empty()

# main server function


def run_server(primary, filename, port, server_id):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    chatbot_pb2_grpc.add_ChatBotServicer_to_server(
        ChatBotServer(primary, filename, server_id), server)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    print("GRPC Server started, listening on ",  port)
    server.wait_for_termination()
