from threading import *


class ServerThread(Thread):
    def __init__(self, socket):
        Thread.__init__(self)
        self.client_socket = socket
        self.start()

    def run(self):
        while True:
            print('Client sent:', self.client_socket.recv(1024).decode())
            self.client_socket.send(b'Oi you sent something to me')
