from threading import *
import re
from memory_manager import MemoryManager

ServerMemory = MemoryManager()

# create regexes for each command in the protocol
create_protocol = re.compile("^CREATE:[a-zA-Z0-9]+:EOM$", re.IGNORECASE)
send_protocl = re.compile("^LOGIN:[a-zA-Z0-9]+:EOM$", re.IGNORECASE)
list_protocol = re.compile("^LIST:[a-zA-Z0-9]+:EOM$", re.IGNORECASE)
send_protocol = re.compile("^SEND:[a-zA-Z0-9]+:[a-zA-Z0-9]+:EOM$", re.IGNORECASE)
delete_protocol = re.compile("^DELETE:[a-zA-Z0-9]+:EOM$", re.IGNORECASE)


protocol_list = [create_protocol, send_protocol, list_protocol, send_protocol, delete_protocol]



class ServerThread(Thread):
    def __init__(self, socket):
        Thread.__init__(self)
        self.client_socket = socket
        self.start()
        self.username = ""


    def create(self,username):
        print("inhere")
        self.username = username
        ServerMemory.create_user(username)


    def run(self):
        buffer = ""

        while True:
            client_msg = self.client_socket.recv(1024).decode()
            buffer += client_msg
            
            for protocol in protocol_list:
                if protocol.fullmatch(buffer):
                    if protocol == create_protocol:
                        self.create(buffer.split(":")[1])
                    buffer = ""


            print("test", "\n" in client_msg)
            print("Client:", client_msg)
            self.client_socket.send(b'Hi Adele')
