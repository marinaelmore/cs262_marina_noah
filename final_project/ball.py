import pygame as pg
from config import *
import threading
import time


class Ball():

    #def __init__(self, player_1, player_2, window):
    def __init__(self, player_1, player_2):
        # Pass paddle and window attributes
        self.player_1 = player_1
        self.current_paddle = player_1.paddle
        self.player_2 = player_2
        self.opponent_paddle = player_2.paddle

        # Initialize Ball
        self.x = WINDOW_WIDTH/2
        self.y = WINDOW_HEIGHT/2
        self.radius = BALL_RADIUS
        self.xspeed = -BALL_SPEED
        self.yspeed = BALL_SPEED
        self.color = BLUE

    def move(self):
        self.x = self.x + self.xspeed
        self.y = self.y + self.yspeed

        self.collisions()
        
        return self.player_1.score, self.player_2.score

    def update_ball(self, window):
        pg.draw.circle(
            window, self.color, (self.x, self.y), self.radius)

    def flash_red(self, window):
        self.color = RED
        self.update_ball(window)
        time.sleep(0.5)
        self.color = BLUE
        self.update_ball(window)

    def collisions(self):

        # Ball moving right
        if self.xspeed > 0:
            # Hit Paddle - TODO
            if self.opponent_paddle.collidepoint(self.x, self.y):
                self.xspeed = -self.xspeed

            # Hit Right Wall
            if self.x >= WINDOW_WIDTH:
                self.xspeed = -self.xspeed
                self.player_1.score = self.player_1.score+1
                # flash red in a different thread using threading
                #threading.Thread(target=self.flash_red).start()

        # Ball moving left
        if self.xspeed < 0:
            # Hit Left Paddle
            if self.current_paddle.collidepoint(self.x, self.y):
                self.xspeed = -self.xspeed

            # Hit Left Wall
            if self.x <= 0:
                self.xspeed = -self.xspeed
                self.player_2.score = self.player_2.score+1
                #threading.Thread(target=self.flash_red).start()

        # Ball Moving Up
        if self.yspeed < 0:
            # Hit Top
            if self.y <= 0:
                self.yspeed = -self.yspeed

        # Ball Moving Down
        if self.yspeed > 0:
            # Hit Bottom
            if self.y >= WINDOW_HEIGHT:
                self.yspeed = -self.yspeed

    def reset_position(self):
        self.x = WINDOW_WIDTH/2
        self.y = WINDOW_HEIGHT/2
