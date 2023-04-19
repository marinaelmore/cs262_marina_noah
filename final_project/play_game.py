import pygame as pg
from pygame.locals import *
from config import *
from random import randint
from player import Player
from ball import Ball


class PongGame():
    def __init__(self, player_id):

        pg.init()

        self.window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        self.curr_player = Player(self.window, player_id=0)
        self.opponent_player = Player(self.window, player_id=1)

        self.ball = Ball(self.curr_player, self.opponent_player, self.window)

        self.font = pg.font.SysFont(None, 24)

    def run_game(self):
        running = True
        while running:
            curr_player_score_img = self.font.render(
                'Player 1: {}'.format(self.curr_player.score), True, BLUE)
            opponent_score_img = self.font.render(
                'Player 2: {}'.format(self.opponent_player.score), True, BLUE)

            for event in pg.event.get():
                if event.type == QUIT:
                    running = False

                if event.type == KEYDOWN:
                    self.curr_player.move(event.key)
                    self.curr_player.update()

            # Window + Score
            self.window.fill(BLACK)
            self.window.blit(curr_player_score_img, (20, 20))
            self.window.blit(opponent_score_img, (WINDOW_WIDTH-100, 20))

            # Paddles
            self.curr_player.update()
            self.opponent_player.update()

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
