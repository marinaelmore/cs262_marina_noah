import pygame as pg
from pygame.locals import *
from config import *

class Player():
    def __init__(self, player_id):
        self.player_id = player_id
        self.score = 0
        self.paddle = self.initialize_paddle()

    def initialize_paddle(self):
        if self.player_id == 0:
            paddle = Rect(PADDLE_WIDTH, WINDOW_HEIGHT/2, PADDLE_WIDTH, PADDLE_HEIGHT)
        elif self.player_id == 1:
            paddle = Rect(WINDOW_WIDTH-PADDLE_WIDTH*2, WINDOW_HEIGHT/2, PADDLE_WIDTH, PADDLE_HEIGHT)

        return paddle

