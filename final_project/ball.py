# Control the ball and movement
# https://gamedev.stackexchange.com/questions/4253/in-pong-how-do-you-calculate-the-balls-direction-when-it-bounces-off-the-paddl


from config import WINDOW_HEIGHT, WINDOW_WIDTH, BALL_SIZE, BALL_SPEED


class Ball():

    def __init__(self):
        self.x = WINDOW_WIDTH/2
        self.y = WINDOW_HEIGHT/2
        self.size = BALL_SIZE
        self.xspeed = BALL_SPEED
        self.yspeed = BALL_SPEED

    def reset_position(self):
        self.x = WINDOW_WIDTH/2
        self.y = WINDOW_HEIGHT/2

    def get_position(self):
        print("Ball pos")
    
    def update_position(self):
        print("Update position")

    def collide_with_paddle(self):
        print("Collide with paddle")

    def collide_with_top(self):
        print("Collide with top")

    def collide_with_bottom(self):
        print("Collide with bottom")

    def collide_with_left_side(self):
        print("Collide with left side - point!")

    def collide_with_right_side(self):
        print("Collide with right slide - point!")

