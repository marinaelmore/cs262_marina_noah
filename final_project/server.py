from concurrent import futures
import threading
import uuid
import queue
import time
import grpc
import proto_files.pong_pb2 as pong
import proto_files.pong_pb2_grpc as pong_grpc
from config import LEFT_PLAYER_ID, LEFT_X, LEFT_Y, RIGHT_PLAYER_ID, RIGHT_X, RIGHT_Y, PADDLE_SPEED, WINDOW_HEIGHT, WINDOW_WIDTH, BALL_SPEED
from game import ServerGame

class PongServer(pong_grpc.PongServerServicer): 

    def __init__(self):

        print("Initializing Server...")
        # create group of players as a queue
        self.players = queue.Queue()
        self.active_games = {}
        self.game_player_1 = None
        self.game_player_2 = None

        # start a thread to pair players
        threading.Thread(target=self.pair_players).start()

        self.game_ready = False

        # Start thread to move the ball
        threading.Thread(target=self.move_ball).start()


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
                self.game_ready = True
            time.sleep(0.1)

    
    def update_player_usernames(self, username, player_id):
        for player, game in self.active_games.items():
             game.update_username(username, player_id) 

    def get_usernames(self, request, context):
        # player_1 = request.player_1_id
        # player_2 =request.player_2_id
        # player_1_username = self.active_games[player_1].get_username()
        # player_2_username = self.active_games[player_2].get_username()
        # yield pong.UserNameMessage(player_1_username=player_1_username, player_2_username=player_2_username)
         print("called")
         yield pong.UserNameMessage(player_1_username="marina", player_2_username="noah")

    def initialize_game(self, request, context):
        print("Initializing Player...")
        player_id = str(uuid.uuid4())
        player_username = request.username
        print(player_id, player_username)
        self.players.put(player_id)

        while player_id not in self.active_games:
            yield  pong.GameReady(ready=False, player_1="", player_2="", first_player = False)
            time.sleep(0.5)

        game = self.active_games[player_id]
        self.game_player_1 = game.player_1
        self.game_player_2 = game.player_2
        first_player = True if player_id == self.game_player_1 else False

        yield pong.GameReady(ready=True, player_1=self.game_player_1, player_2=self.game_player_2, first_player = first_player)

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

    def move_ball(self):
        while not self.game_ready:
            time.sleep(0.5)
        print("Initializing Ball...")
        while True:
            time.sleep(BALL_SPEED/100)
            for player_id in self.active_games:
                game = self.active_games[player_id]
                game.move_ball()
    
    def ball_stream(self, request, context):
        print("Starting ball stream...")
        while True:
            player_id = request.player_id
            game = self.active_games[player_id]
            player_1_score = game.player_objs[self.game_player_1]["game"].score
            player_2_score = game.player_objs[self.game_player_2]["game"].score
            yield pong.BallPosition(x=game.ball.x, y=game.ball.y, xspeed=game.ball.xspeed, yspeed=game.ball.yspeed, player_1_score=player_1_score, player_2_score=player_2_score)
    
def run_server():
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    pong_grpc.add_PongServerServicer_to_server(PongServer(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("GRPC Server started, listening on " + port)
    server.wait_for_termination()