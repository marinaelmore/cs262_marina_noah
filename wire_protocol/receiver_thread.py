from threading import Thread
from time import sleep

class ReceiverThread(Thread):
    
    def __init__(self, socket):
        Thread.__init__(self)
        self.client_socket = socket
        self.start()

    def run(self):
        while True:
            msg = self.client_socket.recv(1024).decode()
            if msg=="": 
                print("\nServer closed unexpectedly")
                break
            print()
            print("------------------------------------")
            print(msg)
            print("------------------------------------")
            