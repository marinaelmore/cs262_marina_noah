from threading import Thread
from time import sleep


# Class responsible for printing incoming messages from the server without blocking the input
class ReceiverThread(Thread):

    def __init__(self, socket):
        Thread.__init__(self)
        self.client_socket = socket
        self.start()

    def run(self):
        while True:
            msg = self.client_socket.recv(1024).decode()
            if msg == "":
                print(f"\nServer closed unexpectedly")
                break
            print()
            print("*** Incoming message from server ***")
            print(msg)
            print("*** Message Received ***")
            print()
