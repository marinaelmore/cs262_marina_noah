import grpc
from .proto_files import pong_pb2
from .proto_files import pong_pb2_grpc
import queue
import threading
from config import PADDLE_SPEED

class PongClient:
    def __init__(self):
        # create a queue to store errors from the receiver thread
        self.receiver_errors = queue.Queue()
        self.player_id = -1


    def client_recieve_ball(self):
        for message in self.conn.BallStream():
            # Display Ball 
            print(message)

    def client_recieve_paddle(self):
        for message in self.conn.PaddleStream():
            # Display Opponent's Paddle
            print(message)


    def run_client(self, host):

        print("Attempting to establish a connection...")

        # create RPC channel and establish connection with the server
        with grpc.insecure_channel(f'{host}:50051') as channel:

            pong_stub = pong_pb2_grpc.PongServerStub(channel)

            # Initialize Starting Position for both player
            initialize_response = pong_stub.initialize_player()

            if initialize_response:
                self.player_id = initialize_response.player_id

                # Based on the current player_id, establish current and opposing positions
            
                # Once complete send response to server. Once server gets both, 


            # Establish listeners for ball and opponents paddle
            ball_reciever = threading.Thread(target=self.client_recieve_ball())
            paddle_reciever = threading.Thread(target=self.client_recieve_paddle())

            response = None
            
            # Run Game
            while True:

                # Get paddle location
                x = 1.67
                y = 0.90
                player_id = self.player_id
                yspeed = PADDLE_SPEED
                
                # Send paddle location
                response = pong_stub.PaddleStream(pong_pb2.PaddlePosition(player_id, x, y, yspeed))


                #if response:
                #    # if the server has set the logged in user, update the client's state
                #    if response.SET_LOGIN_USER:
                #        logged_in_user = response.SET_LOGIN_USER
                #        # login the receiver thread to start reading messages
                #        receiver.login(logged_in_user)
                #    print("\n---------------------------------------------------------")
                #    print(response.message)
                #    print("---------------------------------------------------------\n")