import pygame as pg
from pygame.locals import *
from config import *
from random import randint
from player import Player
from ball import Ball
import threading
import proto_files.pong_pb2 as pong


class PongGame():
    def __init__(self, first_player, player_1, player_2, pong_stub):

        pg.init()

        self.window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

        self.first_player = first_player

        self.pong_stub = pong_stub

        self.player_1 = Player(self.window, player_id = player_1, position=0)
        self.player_2 = Player(self.window, player_id = player_2, position=1)
        
        self.me = self.player_1 if self.first_player  else self.player_2
        self.other = self.player_2 if self.first_player else self.player_1

        self.ball = Ball(self.player_1, self.player_2, self.window)

        self.font = pg.font.SysFont(None, 24)


    def follow_opponent(self):
        for paddle_update in self.pong_stub.paddle_stream(pong.PaddleRequest(player_id=self.other.player_id)):
            self.other.paddle.y = paddle_update.y
            self.other.update()

    def send_movement(self, event_key):
        self.pong_stub.move(pong.PaddleMovement(player_id = self.me.player_id, key = event_key))
    
    def update_score(self):
        player1_score_img = self.font.render(
                'Player 1: {}'.format(self.player_1.score), True, BLUE)
        player2_score_img = self.font.render(
                'Player 2: {}'.format(self.player_2.score), True, BLUE)
        
        self.window.blit(player1_score_img, (20, 20))
        self.window.blit(player2_score_img, (WINDOW_WIDTH-100, 20))

    def run_game(self):
        t = threading.Thread(target=self.follow_opponent).start()
        running = True

        while running:

            for event in pg.event.get():
                if event.type == QUIT:
                    running = False

                if event.type == KEYDOWN:
                    #in another thread send_movemnt
                    t = threading.Thread(target=self.send_movement, args=([event.key])).start()
                    self.me.move(event.key)
                    self.me.update()

            # Window + Score
            self.window.fill(BLACK)
            self.update_score()

            # Paddles
            self.player_1.update()
            self.player_2.update()

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
