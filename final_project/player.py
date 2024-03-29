import pygame as pg
from pygame.locals import K_UP, K_DOWN, Rect
from config import *


dir = {K_UP: -PADDLE_SPEED, K_DOWN:  PADDLE_SPEED}


class Player():
    def __init__(self, window, player_id, position):
        self.player_id = player_id
        self.score = 0
        self.position = position
        self.window = window
        self.paddle = self.initialize_paddle()
        self.username = ""

    def initialize_paddle(self):
        if self.position == 0:
            paddle = Rect(WINDOW_MARGIN, WINDOW_HEIGHT /
                          2, PADDLE_WIDTH, PADDLE_HEIGHT)
        elif self.position == 1:
            paddle = Rect(WINDOW_WIDTH-WINDOW_MARGIN,
                          WINDOW_HEIGHT/2, PADDLE_WIDTH, PADDLE_HEIGHT)

        return paddle

    def move(self, event_key):
        if event_key in dir:
            v = dir[event_key]
            if self.paddle.y <= 0:
                v = max(0, v)
            elif self.paddle.y >= WINDOW_HEIGHT-PADDLE_HEIGHT:
                v = min(0, v)
            self.paddle.move_ip((0, v))

    def update(self):
        pg.draw.rect(self.window, BLUE, self.paddle, PADDLE_WIDTH)
