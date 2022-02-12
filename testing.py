import arcade
from random import randrange
import snake

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

        # Position the food
        food.center_x = randrange(SCREEN_WIDTH)
        food.center_y = randrange(SCREEN_HEIGHT)

        # Add the food to the lists
        self.food_list.append(food)

class BadFood(TestFood):
    def setup(self):
        super().setup()
        for i in range(FOOD_COUNT):
            # Create the food instance
            food = arcade.Sprite("food.png")

            # Position the food
            food.center_x = randrange(SCREEN_WIDTH)
            food.center_y = randrange(SCREEN_HEIGHT)

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
        """Ryan - Initialize sounds"""
        self.init_sounds()

    
    def init_sounds(self):
        self.yum = arcade.load_sound("sounds/yum.mp3")
        self.yuck = arcade.load_sound("sounds/yuck.mp3")

    # sets up the game variables
    def setup(self):
        
        self.snake = snake.Snake(100, 100, 5)
        self.goodfood = GoodFood()
        self.badfood = BadFood()
        #self.background = arcade.load_texture("bg.jpg")
        self.center_window()
        self.goodfood.setup()
        self.badfood.setup()

    # handles drawing for background and sprites
    def on_draw(self):
        # clears previous drawing
        self.clear() 

        # draws the backgound and snake
        #arcade.draw_lrwh_rectangle_textured(0, 0, self.width, self.height, self.background)
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

        for self.goodfood.food in goodfood_collision:
            self.score += 1
            """Ryan - added sound effect"""
            arcade.play_sound(self.yum)
            self.goodfood.setup()
            self.badfood.setup()
            self.snake.grow()

        for self.badfood.food in badfood_collision:
            """Ryan - added sound effect"""
            arcade.play_sound(self.yuck)
            self.badfood.food.remove_from_sprite_lists()


    # handle key press
    def on_key_press(self, symbol, modifiers):
        if (symbol == arcade.key.UP):
            self.snake.x_speed = 0
            self.snake.y_speed = self.snake.speed
        elif (symbol == arcade.key.DOWN):
            self.snake.x_speed = 0
            self.snake.y_speed = -self.snake.speed
        elif (symbol == arcade.key.LEFT):
            self.snake.x_speed = -self.snake.speed
            self.snake.y_speed = 0
        elif (symbol == arcade.key.RIGHT):
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
