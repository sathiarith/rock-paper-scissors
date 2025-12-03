import arcade
from screens import Start

# configuration of game
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Rock, Paper, Scissors"

class Game(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Create views
        self.start_screen = Start()

        self.show_view(self.start_screen)