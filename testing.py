import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = 'First Arcade'

class AlphabetSnakeGame(arcade.Window):
    def __init__(self, width, height, title):
        # call Window class initializer
        super().__init__(width, height, title, resizable=False)
        self.background = None
        self.center_window()
    
    # sets up the game variables
    def setup(self):
        
        self.background = arcade.load_texture("pokemon.jpg")
    
    # handles drawing for background and sprites
    def on_draw(self):
        # clears previous drawing
        self.clear() 

        # draws the backgound
        arcade.draw_lrwh_rectangle_textured(0, 0, self.width, self.height, self.background)

    # for game logic
    def on_update(self, delta_time):
        pass
    
    # handle key press
    def on_key_press(self, symbol, modifiers):
        pass
    
    # handle key release
    def on_key_release(self, symbol, modifiers):
        pass


def main():
    my_game = AlphabetSnakeGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    my_game.setup()
    arcade.run()

if __name__ == '__main__':
    main()
