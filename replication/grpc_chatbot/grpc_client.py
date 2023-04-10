import grpc
from .proto_files import chatbot_pb2
from .proto_files import chatbot_pb2_grpc
from .helpers import receiver_thread
import re
import json
import queue
# A helper method to ensure we get alphanumeric input from the user


def get_alphanumeric_input(prompt):
    alphanumeric = re.compile("[a-zA-Z0-9]+")
    while True:
        user_input = input(prompt)
        if re.fullmatch(alphanumeric, user_input):
            return user_input
        else:
            print("Please only use letters and numbers")


class ChatbotClient:
    def __init__(self):
        self.current_server = 0
        self.receiver_errors = queue.Queue()
        with open('servers.json', 'r') as servers_file:
            # load json
            server_json = json.loads(servers_file.read())
            self.servers = server_json['servers']
            

    def run_client(self):
        while True:
            try:
                self.run_client_attempt()
            except grpc.RpcError as e:
                if e.code() == grpc.StatusCode.PERMISSION_DENIED:
                    print(f"Attempted to contact non-primary server")
                else:
                    print(e.code())
                self.current_server = (self.current_server + 1) % len(self.servers)
                print("new server", self.current_server)
                self.receiver_errors = queue.Queue()
                    

    def run_client_attempt(self):
        # create RPC channel and establish connection with the server
        host = self.servers[self.current_server]['host']
        port = self.servers[self.current_server]['port']
        print(f"Attempting to establish a connection with {host}:{port}...")
        with grpc.insecure_channel(f'{host}:{port}') as channel:

            chatbot_stub = chatbot_pb2_grpc.ChatBotStub(channel)
            response = None


            receiver = receiver_thread.ReceiverThread(chatbot_stub, self.receiver_errors)
            
            # the main difference from the non-grpc client is that we need to keep track of thread specific state
            # on the client (server is stateless). This is akin to how HTTP operates.
            logged_in_user = ""

            while True:
                #check if error queue has anything in it if so raise it
                if not self.receiver_errors.empty():
                    raise self.receiver_errors.get()

                command = input(
                    "Select a Command \n CREATE, LOGIN, LIST, SEND, DELETE:  ").upper()
                
                if not self.receiver_errors.empty():
                    raise self.receiver_errors.get()

                if command == "CREATE":

                    input_username = get_alphanumeric_input(
                        "Create a username [a-zA-Z0-9]: ")

                    response = chatbot_stub.create_user(
                        chatbot_pb2.UserRequest(username=input_username))

                elif command == "LOGIN":

                    username = get_alphanumeric_input(
                        "Login with username [a-zA-Z0-9]: ")

                    response = chatbot_stub.login_user(
                        chatbot_pb2.UserRequest(username=username))

                elif command == "LIST":

                    wildcard = input(
                        "Enter search prefix (or Enter for all accounts): ")

                    response = chatbot_stub.list_users(
                        chatbot_pb2.ListRequest(wildcard=wildcard))

                elif command == "SEND":

                    username = get_alphanumeric_input(
                        "Destination username [a-zA-Z0-9]: ")
                    message = input("Type message: ")

                    # Call server func
                    response = chatbot_stub.send_message(
                        chatbot_pb2.MessageRequest(logged_in_user=logged_in_user, username=username, message=message))

                elif command == "DELETE":

                    username = get_alphanumeric_input(
                        "Enter username to delete [a-zA-Z0-9]: ")

                    # call server func
                    response = chatbot_stub.delete_user(
                        chatbot_pb2.UserRequest(username=username))

                else:
                    print("Invalid command, please try again.")

                if response:
                    # if the server has set the logged in user, update the client's state
                    if response.SET_LOGIN_USER:
                        logged_in_user = response.SET_LOGIN_USER
                        # login the receiver thread to start reading messages
                        receiver.login(logged_in_user)
            
                    print("\n---------------------------------------------------------")
                    print(response.message)
                    print("---------------------------------------------------------\n")
