import pygame as pg
from pygame.locals import *
from config import *
from random import randint
from player import Player
from ball import Ball


dir = {K_LEFT: (0, 0), K_RIGHT: (0, 0), K_UP: (0, -PADDLE_WIDTH), K_DOWN: (0, PADDLE_WIDTH)}

class PongGame():
    def __init__(self, player_id):
        pg.init()

        self.window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        
        self.curr_player = Player(player_id=0)
        self.opponent_player = Player(player_id=1)

        self.ball = Ball(self.curr_player, self.window)

        self.font = pg.font.SysFont(None, 24)


    def run_game(self):
        running = True
        while running:
            player_1_score_img = self.font.render('Player 1: {}'.format(self.curr_player.score), True, BLUE)
            player_2_score_img = self.font.render('Player 2: {}'.format(self.opponent_player.score), True, BLUE)

            for event in pg.event.get():
                if event.type == QUIT:
                    running = False

                if event.type == KEYDOWN:
                    if event.key in dir:
                        v = dir[event.key]
                        self.curr_player.paddle.move_ip(v)

            # Window + Score
            self.window.fill(BLACK)
            self.window.blit(player_1_score_img, (20, 20))
            self.window.blit(player_2_score_img, (WINDOW_WIDTH-100, 20))
            
            # Paddles
            pg.draw.rect(self.window, BLUE, self.curr_player.paddle, PADDLE_WIDTH)
            pg.draw.rect(self.window, BLUE, self.opponent_player.paddle, PADDLE_WIDTH)

            # Ball
            self.ball.move()
            self.ball.update_ball()

            pg.display.flip()                       
    
        pg.quit()


def main():
    pong = PongGame(player_id=0)
    pong.run_game()

if __name__ == "__main__":
     main()