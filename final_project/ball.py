# Control the ball and movement
# https://gamedev.stackexchange.com/questions/4253/in-pong-how-do-you-calculate-the-balls-direction-when-it-bounces-off-the-paddl

import pygame as pg
from config import *
import asyncio

class Ball():

    def __init__(self, current_player, opponent_player, window):
        # Pass paddle and window attributes
        self.current_player = current_player
        self.current_paddle = current_player.paddle
        self.opponent_player = opponent_player
        self.opponent_paddle = opponent_player.paddle
        self.window = window

        # Initialize Ball
        self.x = WINDOW_WIDTH/2
        self.y = WINDOW_HEIGHT/2
        self.radius = BALL_RADIUS
        self.xspeed = -BALL_SPEED
        self.yspeed = BALL_SPEED
        self.color = BLUE

        self.ball = self.initialize_ball()


    def initialize_ball(self):
        ball = pg.draw.circle(self.window, self.color, (self.x, self.y), self.radius)
        return ball

    #async def move(self):
    def move(self):
        self.x = self.x + self.xspeed
        self.y = self.y + self.yspeed

        self.collisions()
    
    def update_ball(self):
        self.ball = pg.draw.circle(self.window, self.color, (self.x, self.y), self.radius)
       
    def collisions(self):

        # Ball moving right
        if self.xspeed > 0:
            # Hit Paddle - TODO
            if self.opponent_paddle.collidepoint(self.x, self.y):
                self.xspeed = -self.xspeed

            # Hit Right Wall
            if self.x >= WINDOW_WIDTH:
                self.xspeed = -self.xspeed
                self.current_player.score = self.current_player.score+1

        # Ball moving left
        if self.xspeed < 0:
            # Hit Left Paddle
            if self.current_paddle.collidepoint(self.x, self.y):
                self.xspeed = -self.xspeed

            # Hit Left Wall
            if self.x <= 0:
                self.xspeed = -self.xspeed
                self.opponent_player.score = self.opponent_player.score+1
        
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
