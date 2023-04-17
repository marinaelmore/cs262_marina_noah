# Classic Pong Game
# Author: Eddie Elvira
# Author's Github page: https://github.com/BlitzyMango/

# Visit https://github.com/BlitzyMango/Pong-Game to find documentation 
# and additional info for this project on the README.md file

import pygame
import asyncio


class pong(object):
    l = 0
    w = 0
    r = 0
    score = [0, 0]

    def __init__(self, paddle_color=(0, 0, 255), ball_color=(255, 255, 255)):
        self.paddle_color = paddle_color
        self.ball_color = ball_color

    @staticmethod
    def event_quit() -> bool:
        for event in pygame.event.get():   # creates a list of events
            if event.type == pygame.QUIT:  # quit game when the user closes the window
                pygame.quit()
                return False
        return True

    @classmethod
    def set_length(cls, length):
        cls.l = length

    @classmethod
    def set_width(cls, width):
        cls.w = width

    @classmethod
    def set_radius(cls, radius):
        cls.r = radius

    @classmethod
    def raise_score(cls, player1):
        if player1:
            cls.score[0] += 1
        else:
            cls.score[1] += 1

    @staticmethod
    async def redrawWindow(win):
        surface = pygame.display.set_mode(win)
        surface.fill((0, 0, 0))  # creates a background (black in this case)
        asyncio.create_task(game.draw(surface))
        pygame.display.update()

    @staticmethod
    async def move():
        p1.move()
        p2.move()
        await b.move()

    def message_box():
        pass

    @staticmethod
    async def draw(surface):
        b.draw_ball(surface)
        p1.draw_paddle(surface)
        p2.draw_paddle(surface)
        game.show_score(surface)
        pygame.display.update()
        await asyncio.sleep(0.01)

    @classmethod
    def show_score(cls, surface):
        font = pygame.font.SysFont(None, 40)  # declare font
        score = font.render(str(cls.score[0]) + ':' + str(cls.score[1]),
                            True, (255, 255, 255))  # format score

        '''Add score and coordinates to top left and right of screen'''
        surface.blit(score, (cls.l // 2 - cls.w // 10, cls.w // 10))


class ball(pong):
    def __init__(self):
        super().__init__()
        self.pos = [pong.l//2, pong.w//2]
        self.dirnx = pong.l//100
        self.dirny = pong.w//100

    async def move(self):
        self.pos = [self.pos[0] + self.dirnx, self.pos[1] + self.dirny]
        await b.horizontal_collision()

    async def horizontal_collision(self):
        asyncio.create_task(b.vertical_collision())
        # If ball is moving right
        if self.dirnx > 0:
            if self.pos[0] + pong.r >= p1.location()[0]:
                y_top1 = p1.location()[1]
                y_bottom1 = y_top1 + p1.length()
                b.paddle_collision(p1, self.pos[1], y_top1, y_bottom1)
            if self.pos[0] + pong.r >= pong.l:
                self.dirnx = -self.dirnx
                game.raise_score(True)

        # If ball is moving left
        if self.dirnx < 0:
            if self.pos[0] - pong.r <= p2.location()[0]+p2.width():
                y_top2 = p2.location()[1]
                y_bottom2 = y_top2 + p2.length()
                b.paddle_collision(p2, self.pos[1], y_top2, y_bottom2)
            if self.pos[0] + pong.r <= 0:
                self.dirnx = -self.dirnx
                game.raise_score(False)

    async def vertical_collision(self):
        # If ball is moving up
        if self.dirny < 0:
            # if ball touches top of screen
            if self.pos[1] <= (pong.r):
                self.dirny = -self.dirny

        # If ball is moving down
        if self.dirny > 0:
            # if ball touches bottom of screen
            if self.pos[1] >= (pong.w-pong.r):
                self.dirny = -self.dirny
        await asyncio.sleep(0)

    def paddle_collision(self, paddle, yball, ytop, ybottom):
        if (yball <= ybottom) and (yball >= ytop):
            self.dirnx = -self.dirnx
            if paddle.velocity() != 0:
                self.dirny = paddle.velocity() // 2

    # def reset(self):
    #     global reset, slope, x_divisor, y_divisor
    #     slope = Fraction((pong.w//2 - self.pos[1]), (pong.l//2 - self.pos[0]))

    #     num_zeros_x = int(math.log10(abs(slope.denominator)))
    #     num_zeros_y = int(math.log10(abs(slope.numerator)))
    #     x_divisor = '1' + ('0'*num_zeros_x)
    #     y_divisor = '1' + ('0'*num_zeros_y)

    #     x = -slope.denominator
    #     y = -slope.numerator

    #     self.dirnx, self.dirny = x//int(x_divisor), y//int(y_divisor)

    #     self.pos = [self.pos[0] + self.dirnx, self.pos[1] + self.dirny]

    #     if self.pos[0] >= pong.l//2-self.dirnx-1 and self.pos[0] <= pong.l//2+self.dirnx+1:
    #         if self.pos[1] >= pong.w//2-self.dirny-1 and self.pos[0] <= pong.w//2+self.dirny+1:
    #             reset = False
    #             slope = 0

    def draw_ball(self, surface):
        circleCenter = (self.pos[0], self.pos[1])
        pygame.draw.circle(surface, self.ball_color, circleCenter, pong.r)


class paddle(pong):
    def __init__(self, player1):
        super().__init__()
        self.player1 = player1

        self.pad_width = pong.l // 40             # width of paddle
        self.pad_length = pong.w // 5              # length of paddle
        self.center = pong.w//2-self.pad_length//2  # y-coordinate used to center paddle
        self.p1_space = pong.l - self.pad_width*3  # space between wall and paddle1
        self.p2_space = self.pad_width*2               # space between wall and paddle2

        if self.player1:
            self.pos = (self.p1_space, self.center)
        else:
            self.pos = (self.p2_space, self.center)

    def location(self):
        return self.pos

    def length(self):
        return self.pad_length

    def width(self):
        return self.pad_width

    def velocity(self):
        return self.dirny

    def move(self, dirny=0):
        self.dirny = dirny
        self.pos = [self.pos[0], self.pos[1] + self.dirny]

        keys = pygame.key.get_pressed()  # records that a key was pressed
        if self.player1:
            if keys[pygame.K_UP]:
                self.dirny = -self.pad_width
            elif keys[pygame.K_DOWN]:
                self.dirny = self.pad_width

        else:
            if keys[pygame.K_w]:
                self.dirny = -self.pad_width
            elif keys[pygame.K_s]:
                self.dirny = self.pad_width

        self.pos[1] += self.dirny

        if self.pos[1] >= pong.w - self.pad_length:
            self.pos[1] -= self.dirny
        elif self.pos[1] <= 0:
            self.pos[1] -= self.dirny

    def draw_paddle(self, surface):
        # x-coordinate of top-left corner of rectangle
        x = self.pos[0]
        # y-coordinate of top-left corner of rectangle
        y = self.pos[1]

        if self.player1:
            pygame.draw.rect(surface, self.paddle_color,
                             (x, y, self.pad_width, self.pad_length))
        else:
            pygame.draw.rect(surface, self.paddle_color,
                             (x, y, self.pad_width, self.pad_length))


if __name__ == '__main__':
    global b, p1, p2, game

    window_length = 750
    window_width = 500
    ball_radius = 8
    win = (window_length, window_width)
    pong.set_length(win[0])
    pong.set_width(win[1])
    pong.set_radius(ball_radius)

    flag = True
    b = ball()
    p1 = paddle(True)
    p2 = paddle(False)
    game = pong()

    pygame.init()
    # create game and background with length x width size
    asyncio.run(game.redrawWindow(win))
    clock = pygame.time.Clock()

    while flag:
        # 50 milliseconds (lower value = faster)
        pygame.time.delay(30)
        clock.tick(60)                  # fps limit (lower value = slower)
        asyncio.run(pong.move())

        # did the user close the window? If so, terminate program
        flag = game.event_quit()
        if not flag:                    # if user closed window, break loop too
            break

        asyncio.run(game.redrawWindow(win))
