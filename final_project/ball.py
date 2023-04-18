# Control the ball and movement
# https://gamedev.stackexchange.com/questions/4253/in-pong-how-do-you-calculate-the-balls-direction-when-it-bounces-off-the-paddl

import pygame as pg
from config import *

class Ball():

    def __init__(self, paddle, window):
        # Pass paddle and window attributes
        self.paddle = paddle
        self.window = window

        # Initialize Ball
        self.x = WINDOW_WIDTH/2
        self.y = WINDOW_HEIGHT/2
        self.radius = BALL_RADIUS
        self.xspeed = BALL_SPEED
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
    
    def update_ball(self):
        self.ball = pg.draw.circle(self.window, self.color, (self.x, self.y), self.radius)
        
        #if self.rect.left < self.field.rect.left:
        #    self.speed[0] = abs(self.speed[0])
        #if self.rect.right > self.field.rect.right:
        #    self.speed[0] = -abs(self.speed[0])

        #if self.rect.top < self.field.rect.top:
        #    self.speed[1] = abs(self.speed[1])
        #if self.rect.bottom > self.field.rect.bottom:
        #    self.speed[1] = -abs(self.speed[1])

        #if self.rect.colliderect(self.pad.rect):
        #    self.speed[0] = abs(self.speed[0]) 


    def reset_position(self):
        self.x = WINDOW_WIDTH/2
        self.y = WINDOW_HEIGHT/2

    def get_position(self):
        print("Ball pos")


    #def update_position(self):
    #    print("Update position")

    #def collide_with_paddle(self):
    #    print("Collide with paddle")

    #def collide_with_top(self):
    #    print("Collide with top")

    #def collide_with_bottom(self):
    #    print("Collide with bottom")

    #def collide_with_left_side(self):
    #    print("Collide with left side - point!")

    #def collide_with_right_side(self):
    #    print("Collide with right slide - point!")

