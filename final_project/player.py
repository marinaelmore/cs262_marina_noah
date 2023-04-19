import pygame as pg
from pygame.locals import K_LEFT, K_RIGHT, K_UP, K_DOWN, Rect
from config import *


dir = {K_LEFT: (0, 0), K_RIGHT: (0, 0), K_UP: (0, -PADDLE_SPEED), K_DOWN: (0, PADDLE_SPEED)}

class Player():
    def __init__(self, window, player_id):
        self.player_id = player_id
        self.score = 0
        self.window = window
        self.paddle = self.initialize_paddle()

    def initialize_paddle(self):
        if self.player_id == 0:
            paddle = Rect(PADDLE_WIDTH, WINDOW_HEIGHT/2, PADDLE_WIDTH, PADDLE_HEIGHT)
        elif self.player_id == 1:
            paddle = Rect(WINDOW_WIDTH-PADDLE_WIDTH*2, WINDOW_HEIGHT/2, PADDLE_WIDTH, PADDLE_HEIGHT)
        return paddle

    # TODO - need to ensure paddle can't go off screen. Possibly switch from move_ip to move like Ball class
    def move(self, event_key):
        if event_key in dir:
            v = dir[event_key]
            self.paddle.move_ip(v)

    def update(self):
        pg.draw.rect(self.window, BLUE, self.paddle, PADDLE_WIDTH)