from player import Player


class Game:
    def __init__(self, player_1, player_2):        
        self.players = {
            player_1: Player(window=None, player_id=player_1, position=0),
            player_2: Player(window=None, player_id=player_2, position=1)
        }


    def move(self, player_id, movement):
        # Update player position
        player = self.players[player_id]
        player.move(movement)
        print("Moved", player.paddle.y)



    
