import grpc
import json
from concurrent import futures
from .proto_files import chatbot_pb2
from .proto_files import chatbot_pb2_grpc
from .helpers.memory_manager import MemoryManager
from .helpers.heartbeat_thread import HeartbeatThread
import time
import threading


# This is the server class which implements the ChatBotServicer
# It is responsible for handling all the requests from the client
# and ensuring replication across the servers
class ChatBotServer(chatbot_pb2_grpc.ChatBotServicer):
    def __init__(self, filename, server_id):
        self.filename = filename
        self.heartbeats = {}
        self.leader = None
        self.primary = False
        self.server_id = server_id

        # connect to other servers as clients
        self.backup_servers = []
        # open servers.json and read in the list of servers
        with open('servers.json', 'r') as servers_file:
            # load json
            server_json = json.loads(servers_file.read())
            # iterate through servers and add the other servers them to the backup_servers list
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
        
        #additonal thread sends a pulse every 0.1 seconds to other servers for leader election
        HeartbeatThread(self.backup_servers, server_id)
        # check if this server is the leader every 0.1 seconds
        threading.Thread(target=self.leader_election).start()

    # function decorator to check if self.primary is true
    # this decorator will be used to ensure that only the primary server can handle requests
    def primary_only(func):
        def wrapper(self, request, context):
            if self.primary:
                return func(self, request, context)
            else:
                #return context error message "Not primary"
                error_message = "Not Primary Server"
                context.abort(grpc.StatusCode.PERMISSION_DENIED, error_message)

                
        return wrapper

    # create a new user 
    @ primary_only
    def create_user(self, request, _context):
        username = request.username
        print("CREATING USER", username)
        result = self.ServerMemory.create_user(username)
        response = "Successfully created user: {}.".format(
            username) if result else "Failure to create user: {}.".format(username)
        return chatbot_pb2.ChatbotReply(message=response)

    # helper method to login a new user by setting the SET_LOGIN_USER header
    @ primary_only
    def login_user(self, request, _context):
        username = request.username
        print("LOGGING IN USER", username)
        if username in self.ServerMemory.users:
            return chatbot_pb2.ChatbotReply(SET_LOGIN_USER=username, message='Sucessfully logged in user: {}.'.format(username))
        else:
            return chatbot_pb2.ChatbotReply(message='Failed to login user: {}'.format(username))

    # send message from one logged in user to another
    @ primary_only
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


    # this method handles diffs sent from the primary server
    # it will update the state of the server with the diff
    def sync_state(self, request, _context):
        print("SYNCING STATE")
        # ignore sync requests from other servers if you are the primary
        if self.primary:
            return chatbot_pb2.Empty()

        self.ServerMemory.sync_state(
            request.from_hash, request.to_hash, request.diff)
        return chatbot_pb2.Empty()

    # will send a full dump of its memory to a new server that is starting up
    # only primary servers can handle this request since we want 
    # to ensure that the new server has the most up to date state
    @ primary_only
    def get_full_state(self, _request, _context):
        print("GET FULL STATE")
        state = json.dumps(self.ServerMemory.memory_to_dict(), sort_keys=True)
        print("sending state", state)
        return chatbot_pb2.FullStateReply(state=state)


# list users matching with a wildcard
    @ primary_only
    def list_users(self, request, _context):
        wildcard = request.wildcard
        print("LISTING USERS", wildcard)
        matches = ", ".join(self.ServerMemory.list_users(wildcard))
        return_msg = "Current users: {}".format(matches)
        return chatbot_pb2.ChatbotReply(message=return_msg)

# read a message that has been sent to the logged in user
    @ primary_only
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
    @ primary_only
    def delete_user(self, request, _context):
        username = request.username
        print("DELETING USER", username)
        if username != "":
            result = self.ServerMemory.delete_user(username)
            response = "Successfully deleted user {}.".format(
                username) if result else "Failed to delete user {}".format(username)
            return chatbot_pb2.ChatbotReply(message=response)

    # when we receive a heartbeat from another server, update the timestamp
    # in self.heartbeats, this is used by leader election to pick the lowest id server
    # that has sent a heartbeat in the last 1 second
    def heartbeat(self, request, _context):
        self.heartbeats[request.server_id] = time.time()
        return chatbot_pb2.Empty()

    def leader_election(self):
        while True:
            # return the server with the lowest id that has sent a heartbeat in the last 1 second
            old_leader = self.leader
            leader = self.server_id
            for server_id, timestamp in self.heartbeats.items():
                if time.time() - timestamp < 0.5:
                    if leader is None or server_id < leader:
                        leader = server_id

            if old_leader != leader:
                print("Leader changed to server", leader)
                print("Heartbeats", self.heartbeats)
            self.leader = leader
            if leader == self.server_id:
                self.primary = True
                self.ServerMemory.set_primary(True)
            else:
                self.primary = False
                self.ServerMemory.set_primary(False)
            time.sleep(0.5)


# main server function

def run_server(filename, server_id):
    try:
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
        port = None
        # gets the port for this server from the servers.json file
        with open('servers.json', 'r') as servers_file:
            # load json
            server_json = json.loads(servers_file.read())
            #get port form server_json.servers where server_id = global_id
            ports = [s["port"] for s in server_json['servers'] if s["global_id"] == server_id]
            if len(ports) != 1:
                raise Exception("Server ID not found")
            port = ports[0]

        chatbot_pb2_grpc.add_ChatBotServicer_to_server(
            ChatBotServer(filename, server_id), server)
        server.add_insecure_port(f"[::]:{port}")
        server.start()
        print("GRPC Server started, listening on ",  port)
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(0)
        print("Stopping server")
