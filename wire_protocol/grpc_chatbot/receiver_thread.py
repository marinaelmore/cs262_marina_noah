from threading import Thread
from time import sleep
from . import chatbot_pb2


class ReceiverThread(Thread):

    def __init__(self, grpc):
        Thread.__init__(self)
        self.client_grpc = grpc
        self.start()

    def run(self):
        while True:
            response = self.client_grpc.get_message(chatbot_pb2.GetRequest())
            if response.message != "":
                print()
                print("*** Incoming message from server ***")
                print(response.message)
                print("*** Message Received ***")
                print()
            sleep(1)
