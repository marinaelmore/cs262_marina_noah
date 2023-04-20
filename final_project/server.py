from concurrent import futures
import os
import grpc
import proto_files.pong_pb2 as pong
import proto_files.pong_pb2_grpc as pong_grpc
from config import LEFT_PLAYER_ID, LEFT_X, LEFT_Y, RIGHT_PLAYER_ID, RIGHT_X, RIGHT_Y, PADDLE_SPEED
import threading
from random import randint
import uuid
import queue
from game import ServerGame
import time


class PongServer(pong_grpc.PongServerServicer): 

    def __init__(self):

        print("Initializing Server...")
        # create group of players as a queue
        self.players = queue.Queue()
        self.active_games = {}

        # start a thread to pair players
        threading.Thread(target=self.pair_players).start()

        

    def pair_players(self):
        # try and pull two players from the queue
        # if there are not two players, wait for two players
        # if there are two players, pair them up and start the game
        print("Pairing Players...")
        while True:
            if self.players.qsize() % 2 == 0:
                player_1 = self.players.get()
                player_2 = self.players.get()
                #create a tuple of players with player_1 < player_2
                game = ServerGame(player_1, player_2)
                self.active_games[player_1] = game
                self.active_games[player_2] = game
                print("Players paired: ", player_1, player_2)
            time.sleep(0.1)

    def initialize_game(self, request, context):
        print("Initializing Player...")
        player_id = str(uuid.uuid4())
        print(player_id, type(player_id))
        self.players.put(player_id)
        while player_id not in self.active_games:
            yield  pong.GameReady(ready=False, player_1="", player_2="", first_player = False)
            time.sleep(0.5)
        game = self.active_games[player_id]
        game_player_1 = game.player_1
        game_player_2 = game.player_2
        first_player = True if player_id == game_player_1 else False
        yield pong.GameReady(ready=True, player_1=game_player_1, player_2=game_player_2, first_player = first_player)

    def paddle_stream(self, request, context):
        player_id = request.player_id
        game = self.active_games[player_id]
        # wait on condition variable for player
        condition = game.player_objs[player_id]["push"]
        player = game.player_objs[player_id]["game"]
        with condition:
            while True:
                condition.wait()
                yield pong.PaddlePosition(player_id = player_id, y=player.paddle.y)


    def move(self, request, context):
        player_id = request.player_id
        movement = request.key
        game = self.active_games[player_id]
        game.move(player_id, movement)
        return pong.Empty()
        


    

        


def run_server():
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    pong_grpc.add_PongServerServicer_to_server(PongServer(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("GRPC Server started, listening on " + port)
    server.wait_for_termination()