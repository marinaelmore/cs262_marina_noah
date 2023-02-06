from threading import *
import re
from memory_manager import MemoryManager
import select
from wire_protocol import WireProtocol

ServerMemory = MemoryManager()


class ServerThread(Thread):

    def __init__(self, socket):
        Thread.__init__(self)
        self.client_socket = socket
        self.logged_in_user = ""
        self.start()

    def create(self, username):
        print("CREATING USER", username)
        result = ServerMemory.create_user(username)
        response = "CREATE:SUCCESS:EOM" if result else "CREATE:FAILURE:EOM"
        self.client_socket.send(response.encode())

    def login(self, username):
        print("LOGGING IN USER", username)
        if username in ServerMemory.users:
            self.logged_in_user = username
            self.client_socket.send(b'LOGIN:SUCCESS:EOM')
        else:
            self.client_socket.send(b'LOGIN:FAILURE:EOM')

    def send(self, to, message):
        print("SENDING MESSAGE", message, "TO", to)
        if self.logged_in_user != "":
            call_result = ServerMemory.send_message(to, message)
            response = "SEND:SUCCESS:EOM" if call_result else "SEND:FAILURE:EOM"
            self.client_socket.send(response.encode())
        else:
            self.client_socket.send(b'SEND:FAILURE:LOGIN_REQUIRED:EOM')

    def list_users(self, wildcard):
        print("LISTING USERS", wildcard)
        matches = ", ".join(ServerMemory.list_users(wildcard))
        return_msg = "LIST:{}:EOM".format(matches)
        self.client_socket.send(bytes(return_msg, "utf-8"))

    def read_messages(self):
        if self.logged_in_user == "":
            return
        msg = ServerMemory.get_message(self.logged_in_user)
        if msg:
            self.client_socket.send(bytes(msg, "utf-8"))

    def delete(self, username):
        print("DELETING USER", username)
        if username != "":
            ServerMemory.delete_user(username)
            self.client_socket.send(b'DELETE:SUCCESS:EOM')

    def run(self):
        buffer = b""

        while True:
            self.read_messages()
            client_sockets, _, _ = select.select(
                [self.client_socket], [], [], 0.1)
            # this code assumes only one client socket, if more in this
            # thread, will need to use multiple buffers
            for socket in client_sockets:
                client_msg = socket.recv(1024)
                if client_msg == b"":
                    print("Client closed unexpectedly")
                    return
                buffer += client_msg

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
                if len(buffer) > WireProtocol.MAX_BYTES:
                    buffer = b""
