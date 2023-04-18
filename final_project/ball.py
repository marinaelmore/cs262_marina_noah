# Control the ball and movement
# https://gamedev.stackexchange.com/questions/4253/in-pong-how-do-you-calculate-the-balls-direction-when-it-bounces-off-the-paddl

import pygame as pg
from config import *

class Ball():

    def __init__(self, paddle, window):
        # Initialize Ball
        self.x = WINDOW_WIDTH/2
        self.y = WINDOW_HEIGHT/2
        self.size = BALL_SIZE
        self.xspeed = BALL_SPEED
        self.yspeed = BALL_SPEED
        self.color = BLUE

        # Pass paddle and window attributes
        self.paddle = paddle
        self.window = window

    
    def draw_ball(self):
        ball = pg.draw.circle()

    async def move(self):
        self.x = self.x+self.xspeed
        self.y = self.y+self.yspeed

        await self.collison()

    def reset_position(self):
        self.x = WINDOW_WIDTH/2
        self.y = WINDOW_HEIGHT/2

    def get_position(self):
        print("Ball pos")


class Ball():
    def __init__(self, pos, field, pad):
        self.pos = pos
        self.field = field
        self.pad = pad
        self.speed = [1, 1]
        self.color = RED
        self.rect = pygame.Rect(pos, (20, 20))

    def update(self):
        self.rect.move_ip(self.speed)

        if self.rect.left < self.field.rect.left:
            self.speed[0] = abs(self.speed[0])
        if self.rect.right > self.field.rect.right:
            self.speed[0] = -abs(self.speed[0])

        if self.rect.top < self.field.rect.top:
            self.speed[1] = abs(self.speed[1])
        if self.rect.bottom > self.field.rect.bottom:
            self.speed[1] = -abs(self.speed[1])

        if self.rect.colliderect(self.pad.rect):
            self.speed[0] = abs(self.speed[0])

    def draw(self):
        pygame.draw.rect(App.screen, self.color, self.rect, 0)


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

