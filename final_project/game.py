from player import Player
from ball import Ball
import threading

class ServerGame:
    def __init__(self, player_1, player_2):       
        self.player_1 = player_1
        self.player_2 = player_2 
        self.player_objs = {
            player_1: {
            "game": Player(window=None, player_id=player_1, position=0),
            "push": threading.Condition(),
            },
            player_2: {
            "game": Player(window=None, player_id=player_2, position=1),
            "push": threading.Condition(),
            }
        }
        self.ball = Ball(self.player_objs[player_1]["game"], self.player_objs[player_2]["game"])


    def move(self, player_id, movement):
        # Update player position
        player = self.player_objs[player_id]
        player["game"].move(movement)
        cond = player["push"]
        with cond:
            cond.notify()

    def move_ball(self):
        # Update ball position
        self.ball.move()