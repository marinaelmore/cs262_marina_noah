import grpc
import pong_pb2 as pong
import pong_pb2_grpc
import queue
import threading
from config import PADDLE_SPEED
from play_game import PongGame

class PongClient:
    def __init__(self):
        # create a queue to store errors from the receiver thread
        self.receiver_errors = queue.Queue()
        self.player_id = None


    def run_client(self, host):

        print("Attempting to establish a connection...")

        # create RPC channel and establish connection with the server
        with grpc.insecure_channel(f'{host}:50051') as channel:

            pong_stub = pong_pb2_grpc.PongServerStub(channel)

            print("Waiting for another player", end="")
            for game_ready in pong_stub.initialize_game(pong.Empty()):
                if not game_ready.ready:
                    print(".", end="",flush=True)
                else:
                    print("\nPartner found!")
                    self.first_player = game_ready.first_player
                    self.player_1 = game_ready.player_1
                    self.player_2 = game_ready.player_2
                    break
            
            pong_game = PongGame(self.first_player, self.player_1, self.player_2,pong_stub)
            pong_game.run_game()
            
            
            
