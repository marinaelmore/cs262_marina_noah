from concurrent import futures

import grpc
import proto_files.pong_pb2 as pong
import proto_files.pong_pb2_grpc as pong_grpc
from config import LEFT_PLAYER_ID, LEFT_X, LEFT_Y, RIGHT_PLAYER_ID, RIGHT_X, RIGHT_Y, PADDLE_SPEED

class PongServer(pong_grpc.PongServerServicer): 

    def __init__(self):

        print("Initializing Server...")
        self.left_player = False
        self.right_player = False


    def BallStream(self, ball_request, context):
        
        while context.is_active():
            
            ball_x = ball_request.x
            ball_y = ball_request.y

            # Update ball position
    

    def initialize_player(self, request, _context):
        if not self.left_player:
            player_id = LEFT_PLAYER_ID
            self.left_player = True
        elif not self.right_player:
            player_id = RIGHT_PLAYER_ID
            self.right_player = True
        else:
            print("Error")

        return pong.Player(message=pong.Player(player_id=player_id))


def run_server():
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=5))
    pong_grpc.add_PongServerServicer_to_server(PongServer(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("GRPC Server started, listening on " + port)
    server.wait_for_termination()