import pygame as pg
from pygame.locals import QUIT, KEYDOWN
from config import *
from player import Player
from ball import Ball
import asyncio


class PongGame():

    def __init__(self, player_id):

        pg.init()

        self.window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        
        self.curr_player = Player(self.window, player_id=player_id)
        self.opponent_player = Player(self.window, player_id=1)

        self.ball = Ball(self.curr_player, self.opponent_player, self.window)

        self.font = pg.font.SysFont(None, 24)


    def display_score(self):
        curr_player_score_img = self.font.render('Player 1: {}'.format(self.curr_player.score), True, BLUE)
        opponent_score_img = self.font.render('Player 2: {}'.format(self.opponent_player.score), True, BLUE)
        self.window.blit(curr_player_score_img, (20, 20))
        self.window.blit(opponent_score_img, (WINDOW_WIDTH-100, 20))

    async def move_ball(self):
        while True:
            self.ball.move()
            self.ball.update_ball() # render in client

    async def run_game(self):
        print("Run")

        for event in pg.event.get():

            if event.type == KEYDOWN:
                self.curr_player.move(event.key)

        
        await self.ball.move()

            # Window + Score
            #self.window.fill(BLACK)
            #self.display_score()
            
            # Paddles
            #self.curr_player.update() # update with keyboard movement
            #self.opponent_player.update() # update with other players movement

            # Ball
            #self.ball.move() # this information should be streamed to both clients
            #self.ball.update_ball() # render in client

            #pg.display.flip()                  
    
    async def update_objects(self):
        print("update objs")
        self.display_score()
        self.ball.update_ball() # render in client
        self.curr_player.update() # update with keyboard movement
        self.opponent_player.update() # update with other players movement
        pg.display.flip()

    async def render_window(self):
        print("Render")
        self.window.fill(BLACK)
        asyncio.create_task(self.update_objects())
        pg.display.flip()

def main():

    pong = PongGame(player_id=0)
    
    #loop = asyncio.get_event_loop()

    #loop.create_task(pong.render_window())
    #loop.create_task(pong.run_game())

    #try:
    #    loop.run_forever()
    #except KeyboardInterrupt:
    #    pg.quit()

    #await asyncio.gather(pong.render_window(), pong.run_game())

    try:
        while True:
            asyncio.run(pong.render_window())
            asyncio.run(pong.run_game())
    except KeyboardInterrupt:
        pg.quit()


if __name__ == "__main__":
    main()