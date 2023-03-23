from threading import *
from helpers.memory_manager import MemoryManager
import select
from .wire_protocol import WireProtocol

# initialize server memory that is shared across all threads
ServerMemory = MemoryManager()


# create thread-level client connection handler
class ServerThread(Thread):

    def __init__(self, socket):
        Thread.__init__(self)
        self.client_socket = socket
        # a connection is "logged in" by setting logged_in_user to a valid username
        self.logged_in_user = ""
        self.start()

    # Create a new user
    def create(self, username):
        print("CREATING USER", username)
        result = ServerMemory.create_user(username)
        response = "CREATE:SUCCESS:EOM" if result else "CREATE:FAILURE:EOM"
        self.client_socket.send(response.encode())

   # Login a new user
    def login(self, username):
        print("LOGGING IN USER", username)
        if username in ServerMemory.users:
            self.logged_in_user = username
            self.client_socket.send(b'LOGIN:SUCCESS:EOM')
        else:
            self.client_socket.send(b'LOGIN:FAILURE:EOM')

    # send message from a logged in user to another valid user
    def send(self, to, message):
        print("SENDING MESSAGE", message, "TO", to)
        if self.logged_in_user != "":
            call_result = ServerMemory.send_message(
                self.logged_in_user, to, message)
            response = "SEND:SUCCESS:EOM" if call_result else "SEND:FAILURE:EOM"
            self.client_socket.send(response.encode())
        else:
            self.client_socket.send(b'SEND:FAILURE:LOGIN_REQUIRED:EOM')

# list all users that match a wildcard
    def list_users(self, wildcard):
        print("LISTING USERS", wildcard)
        matches = ", ".join(ServerMemory.list_users(wildcard))
        return_msg = "LIST:{}:EOM".format(matches)
        self.client_socket.send(bytes(return_msg, "utf-8"))

# read any messages that have been sent to the logged in user
    def read_messages(self):
        if self.logged_in_user == "":
            return
        msg = ServerMemory.get_message(self.logged_in_user)
        if msg:
            self.client_socket.send(bytes(msg, "utf-8"))

# delete a user
    def delete(self, username):
        print("DELETING USER", username)
        if username != "":
            result = ServerMemory.delete_user(username)
            response = "DELETE:SUCCESS:EOM" if result else "DELETE:FAILURE:EOM"
            self.client_socket.send(bytes(response, "utf-8"))

# main thread loop
    def run(self):
        buffer = b""

        while True:
            # At every iteration, checks if there are any messages to be read
            self.read_messages()
            # check if there are any messages from the client (non-blocking)
            client_sockets, _, _ = select.select(
                [self.client_socket], [], [], 0.1)
            # this code assumes only one client socket, if more in this
            # thread, will need to use multiple buffers
            for socket in client_sockets:
                client_msg = socket.recv(1024)
                if client_msg == b"":
                    print("Client closed unexpectedly")
                    return
                # since messages can come in over multiple packets, we need to buffer them
                buffer += client_msg
                # deserialize and check if we have a complete message
                match = WireProtocol.deserialize_request(buffer)
                if match:
                    command, *args = match
                    if command == "CREATE":
                        self.create(args[0])
                    elif command == "LOGIN":
                        self.login(args[0])
                    elif command == "LIST":
                        self.list_users(args[0])
                    elif command == "SEND":
                        self.send(args[0], args[1])
                    elif command == "DELETE":
                        self.delete(args[0])
                    buffer = b""
                # if we have a message larger than our protocol, an error happened, and we clear the buffer
                if len(buffer) > WireProtocol.MAX_BYTES:
                    buffer = b""
