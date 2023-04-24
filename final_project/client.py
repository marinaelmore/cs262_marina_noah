import grpc
import proto_files.pong_pb2 as pong
import proto_files.pong_pb2_grpc as pong_pb2_grpc
import queue
import threading
from config import PADDLE_SPEED
from client_game import PongGame
from textinput import TextInputGame


class PongClient:
    def __init__(self):
        # create a queue to store errors from the receiver thread
        self.receiver_errors = queue.Queue()
        self.player_id = None


    def get_player_name(self):
        text_input = TextInputGame("Enter your username: ")
        username = text_input.main_loop()
        return username

    def run_client(self, host):

        print("Attempting to establish a connection...")

        # create RPC channel and establish connection with the server
        with grpc.insecure_channel(f'{host}:50051') as channel:

            pong_stub = pong_pb2_grpc.PongServerStub(channel)

            my_username = self.get_player_name()

            print("Waiting for another player", end="")
            for game_ready in pong_stub.initialize_game(pong.UserName(username=my_username)):
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
            
            
            
