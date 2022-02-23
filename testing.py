import arcade
from random import randrange
import snake
from time import sleep

# Defines the number of bad_food items
FOOD_COUNT = 10

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800
SCREEN_TITLE = 'Alphabet Snake'

# Class for food items
class TestFood():
    def __init__(self):
        self.food_list = None

    def setup(self):
        self.food_list = arcade.SpriteList()

    def draw(self):
        self.food_list.draw()

class GoodFood(TestFood):
    def setup(self):
        super().setup()
        # Create the food instance
        food = arcade.Sprite("good_food.png")

        # Position the good food
        food.center_x = randrange(100, SCREEN_WIDTH - 100)
        food.center_y = randrange(300, SCREEN_HEIGHT - 50)

        # Add the food to the lists
        self.food_list.append(food)

class BadFood(TestFood):
    def setup(self):
        super().setup()
        for i in range(FOOD_COUNT):
            # Create the food instance
            food = arcade.Sprite("food.png")

            # Position the bad food
            food.center_x = randrange(100, SCREEN_WIDTH - 100)
            food.center_y = randrange(300, SCREEN_HEIGHT - 50)

            # Add the food to the lists
            self.food_list.append(food)

class TestGame(arcade.Window):
    def __init__(self, width, height, title):
        # call Window class initializer
        super().__init__(width, height, title, resizable=False)
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
        self.bg_music.play(loop=True)

    # sets up the game variables
    def setup(self):
        
        """Ryan 2/2/2022 - updated to new parameters"""
        self.snake = snake.Snake(100, 300, 5)
        self.goodfood = GoodFood()
        self.badfood = BadFood()
        self.background = arcade.load_texture("blackboard.jpg")            #Erik testing blackboard.jpg
        self.center_window()
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
            sleep(1)
            quit()

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

def main():
    my_game = TestGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    my_game.setup()
    my_game.set_update_rate(1/20)
    arcade.run()

if __name__ == '__main__':
    main()
