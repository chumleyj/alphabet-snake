import arcade
import food
import snake
from time import sleep

# Defines the number of bad_food items
FOOD_COUNT = 10

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800
SCREEN_TITLE = 'Alphabet Snake'

"""Ryan 2/24/2022 - Change from arcade.Window to arcade.View and TestGame to TestView"""
class TestView(arcade.View):
    """Ryan 2/24/2022 - Remove width, height, title from __init__"""
    def __init__(self):
        # call Window class initializer
        """Ryan 2/24/2022 - Remove width, height, title, resizable=False"""
        super().__init__()
        self.background = None
        self.score = 0
        self.snake = None
        self.goodfood = None
        self.badfood = None
        # Initializes sound and music
        self.init_sounds()

    def init_sounds(self):
        self.yum = arcade.load_sound("sounds/yum.mp3")
        self.yuck = arcade.load_sound("sounds/yuck.mp3")
        self.bg_music = arcade.load_sound("sounds/bg_music.mp3")
        """Ryan 2/24/2022- loop=True caused issues when player restarted play; removed for now"""
        self.media_player = self.bg_music.play()

    # sets up the game variables
    def setup(self):
        self.snake = snake.Snake(100, 300, 5)
        self.goodfood = food.GoodFood()
        self.badfood = food.BadFood()
        self.background = arcade.load_texture("blackboard.jpg")            #Erik testing blackboard.jpg
        self.goodfood.setup()
        self.badfood.setup()

    # handles drawing for background and sprites
    def on_draw(self):
        # clears previous drawing
        self.clear() 

        # draws the backgound and snake
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH , SCREEN_HEIGHT, self.background)
        
        self.snake.draw()
        self.goodfood.draw()
        self.badfood.draw()

        arcade.draw_text(f'Score: {self.score}', 20, SCREEN_HEIGHT-20, arcade.csscolor.WHITE, 12, font_name='arial')


    # for game logic
    def on_update(self, delta_time):
        self.snake.update()

        """Jeff - updated collision handling"""
        for seg in self.snake.snake_list:
            goodfood_collision = arcade.check_for_collision_with_list(seg, self.goodfood.food_list)
            if goodfood_collision:
                break

        for seg in self.snake.snake_list:
            badfood_collision = arcade.check_for_collision_with_list(seg, self.badfood.food_list)
            if badfood_collision:
                break

        # Checks if the snake collides with itself
        snake_collision = arcade.check_for_collision_with_list(self.snake.snake_head, self.snake.snake_list)

        # If the snake eats good food, score increases, gives sound effect, and all food resets        
        for self.goodfood.food in goodfood_collision:
            self.score += 1
            arcade.play_sound(self.yum)
            self.goodfood.setup()
            self.badfood.setup()

        # If the snake eats bad food, it grows, gives sound effect, and the food disappears
        for self.badfood.food in badfood_collision:
            self.snake.grow()
            arcade.play_sound(self.yuck)
            self.badfood.food.remove_from_sprite_lists()

        # If snake collides with itself, the game quits
        for seg in snake_collision:
            arcade.play_sound(self.yuck)
            """Ryan 2/24/2022 - Updated"""
            # Stops music when player dies
            self.media_player.pause()
            # Brings up Game Over screen
            view = GameOverView()
            self.window.show_view(view)

    # handle key press
    def on_key_press(self, symbol, modifiers):
        if (symbol == arcade.key.UP and self.snake.y_speed >= 0):
            self.snake.x_speed = 0
            self.snake.y_speed = self.snake.speed
        elif (symbol == arcade.key.DOWN and self.snake.y_speed <= 0):
            self.snake.x_speed = 0
            self.snake.y_speed = -self.snake.speed
        elif (symbol == arcade.key.LEFT and self.snake.x_speed <= 0):
            self.snake.x_speed = -self.snake.speed
            self.snake.y_speed = 0
        elif (symbol == arcade.key.RIGHT and self.snake.x_speed >= 0):
            self.snake.x_speed = self.snake.speed
            self.snake.y_speed = 0

    
    # handle key release
    def on_key_release(self, symbol, modifiers):
        pass

"""Ryan 2/24/2022- Added StartView"""
# Class for the starting view that will show once a user loads the game
class StartView(arcade.View):

    def on_show(self):
        # Sets the background color of the StartView
        arcade.set_background_color(arcade.csscolor.BLACK)

    def on_draw(self):
        self.clear()
        # Draws text on the screen
        arcade.draw_text("Alphabet Snake", self.window.width / 2, self.window.height / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Click to advance", self.window.width / 2, self.window.height / 2-75,
                         arcade.color.WHITE, font_size=20, anchor_x="center")

    # Will go to main gameplay once they click on the screen
    def on_mouse_press(self, _x, _y, _button, _modifiers):
        test_view = TestView()
        test_view.setup()
        self.window.show_view(test_view)    

"""Ryan 2/24/2022 - added GameOverView for when the player dies"""
# Screen that shows once a player dies
class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()
        # Background image that populates once the player dies
        self.texture = arcade.load_texture("images/game_over.jpg")

    def on_draw(self):
        self.clear()
        # Populates the screen with the background image
        self.texture.draw_sized(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                                SCREEN_WIDTH, SCREEN_HEIGHT)

    # Allows the user to return to normal gameplay by clicking the screen
    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = TestView()
        game_view.setup()
        self.window.show_view(game_view)

def main():
    """Ryan 2/24/2022 - changed this stuff from windows to views"""
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.center_window()
    start_view = StartView()
    window.show_view(start_view)
    window.set_update_rate(1/20)
    arcade.run()

if __name__ == '__main__':
    main()
