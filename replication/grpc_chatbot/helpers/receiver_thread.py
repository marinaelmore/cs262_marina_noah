from threading import Thread
from time import sleep
from ..proto_files import chatbot_pb2
import grpc

class ReceiverThread(Thread):

    def __init__(self, grpc, receiver_error_queue):
        Thread.__init__(self)
        self.client_grpc = grpc
        # keep track of the logged in user at the client thread level
        self.logged_in_user = ""
        self.start()
        self.error_queue = receiver_error_queue

    # helper method to login the receiver thread
    def login(self, logged_in_user):
        self.logged_in_user = logged_in_user

    def run(self):
        while True:
            try: 
                # every 1/5 second check if we have any inbound messages
                response = self.client_grpc.get_message(
                    chatbot_pb2.GetRequest(logged_in_user=self.logged_in_user))
                if response.message != "":
                    print("\n")
                    print("---------------------------------------------------------")
                    print("You have recieved a message: {}".format(response.message))
                    print("---------------------------------------------------------")
                    print("\n")
                sleep(0.2)
            except grpc.RpcError as e:
                self.error_queue.put(e)
                break
