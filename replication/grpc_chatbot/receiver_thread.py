from threading import Thread
from time import sleep
from . import chatbot_pb2


class ReceiverThread(Thread):

    def __init__(self, grpc):
        Thread.__init__(self)
        self.client_grpc = grpc
        # keep track of the logged in user at the client thread level
        self.logged_in_user = ""
        self.start()

    # helper method to login the receiver thread
    def login(self, logged_in_user):
        self.logged_in_user = logged_in_user

    def run(self):
        while True:
            # every one second check if we have any inbound messages
            response = self.client_grpc.get_message(
                chatbot_pb2.GetRequest(logged_in_user=self.logged_in_user))
            if response.message != "":
                print("\n")
                print("---------------------------------------------------------")
                print("You have recieved a message: {}".format(response.message))
                print("---------------------------------------------------------")
                print("\n")
            sleep(1)
