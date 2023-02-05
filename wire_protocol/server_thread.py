from threading import *
import re
from memory_manager import MemoryManager
import select

ServerMemory = MemoryManager()

# create regexes for each command in the protocol
create_protocol = re.compile("^CREATE:([a-zA-Z0-9]+):EOM$", re.IGNORECASE)
login_protocol = re.compile("^LOGIN:([a-zA-Z0-9]+):EOM$", re.IGNORECASE)
list_protocol = re.compile("^LIST:([a-zA-Z0-9]+):EOM$", re.IGNORECASE)
send_protocol = re.compile("^SEND:([a-zA-Z0-9]+):(.+):EOM$", re.IGNORECASE)
delete_protocol = re.compile("^DELETE:([a-zA-Z0-9]+):EOM$", re.IGNORECASE)


protocol_list = [create_protocol, login_protocol, send_protocol, list_protocol, send_protocol, delete_protocol]



class ServerThread(Thread):
    
    def __init__(self, socket):
        Thread.__init__(self)
        self.client_socket = socket
        self.username = ""
        self.start()
        

    def create(self,username):
        print("CREATING USER", username)
        ServerMemory.create_user(username)
        self.client_socket.send(b'CREATE:SUCCESS:EOM')

    def login(self,username):
        print("LOGGING IN USER", username)
        if username in ServerMemory.users:
            self.username = username
            self.client_socket.send(b'LOGIN:SUCCESS:EOM')
        else:
            self.client_socket.send(b'LOGIN:FAILURE:EOM')

    def send(self, to, message):
        print("SENDING MESSAGE", message, "TO", to)
        if to in ServerMemory.users:
            ServerMemory.users[to].add_message(message)
            self.client_socket.send(b'SEND:SUCCESS:EOM')
        else:
            self.client_socket.send(b'SEND:FAILURE:EOM')

    def list_users(self, wildcard):
        print("LISTING USERS", wildcard)
        matches = ", ".join(ServerMemory.list_users(wildcard))
        return_msg = "LIST:{}:EOM".format(matches)
        self.client_socket.send(bytes(return_msg,"utf-8"))

    def read_messages(self):
        if self.username == "":
            return
        msg = ServerMemory.get_message(self.username)
        if msg:
            self.client_socket.send(bytes(msg,"utf-8"))

    def delete(self,username):
        print("DELETING USER", username)
        if username != "":
            ServerMemory.delete_user(username)
            self.client_socket.send(b'DELETE:SUCCESS:EOM')

    def run(self):
        buffer = ""

        while True:
            self.read_messages()

            client_sockets, _, _ = select.select([self.client_socket], [],[], 0.1)

            for socket in client_sockets:
                client_msg = self.client_socket.recv(1024).decode()
                buffer += client_msg
                
                for protocol in protocol_list:
                    m = protocol.fullmatch(buffer)
                    if m:
                        if protocol == create_protocol:
                            self.create(m[1])
                        elif protocol == login_protocol:
                            self.login(m[1])
                        elif  protocol == list_protocol:
                            self.list_users(m[1])
                        elif protocol == send_protocol:
                            self.send(m[1], m[2])
                        elif protocol == delete_protocol:
                            self.delete(m[1])
                        buffer = ""


