import pygame as pg
from pygame.locals import *
from config import *
from random import randint


class PlayPong():
    def __init__(self) -> None:
        pass

RED = (255, 0, 0)
BLUE = (51, 153, 255)
BLACK = (0, 0, 0)

pg.init()

SIZE = WINDOW_WIDTH, WINDOW_HEIGHT
screen = pg.display.set_mode(SIZE)

paddle1 = Rect(PADDLE_WIDTH, WINDOW_HEIGHT/2, PADDLE_WIDTH, PADDLE_HEIGHT)
paddle2 = Rect(WINDOW_WIDTH-PADDLE_WIDTH*2, WINDOW_HEIGHT/2, PADDLE_WIDTH, PADDLE_HEIGHT)
dir = {K_LEFT: (0, 0), K_RIGHT: (0, 0), K_UP: (0, -PADDLE_WIDTH), K_DOWN: (0, PADDLE_WIDTH)}

font = pg.font.SysFont(None, 24)

running = True

while running:
    player_1_score = 0
    player_2_score = 0
    player_1_score_img = font.render('Player 1: {}'.format(player_1_score), True, BLUE)
    player_2_score_img = font.render('Player 2: {}'.format(player_2_score), True, BLUE)

    for event in pg.event.get():
        if event.type == QUIT:
            running = False
        
        if event.type == KEYDOWN:
            if event.key in dir:
                v = dir[event.key]
                paddle1.move_ip(v)
    
    screen.fill(BLACK)
    screen.blit(player_1_score_img, (20, 20))
    screen.blit(player_2_score_img, (WINDOW_WIDTH-100, 20))
    pg.draw.rect(screen, BLUE, paddle1, PADDLE_WIDTH)
    pg.draw.rect(screen, BLUE, paddle2, PADDLE_WIDTH)
    pg.display.flip()


pg.quit()

#if __name__ == "__main__":
#     main()