import arcade
from random import randrange
import snake

"""Ryan 2 - Sets total number of food items"""
FOOD_COUNT = 10

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800
SCREEN_TITLE = 'Alphabet Snake'

# Class for food items
class TestFood():
    def __init__(self):
        """RYAN 2 - Creates a Sprite list for all the food items"""
        self.food_list = None

    """"RYAN 2 - Creates number of food set to FOOD_COUNT at random locations"""
    def setup(self):
        self.food_list = arcade.SpriteList()

    def draw(self):
        """Ryan2 - draws the food items"""
        self.food_list.draw()

"""RYAN2 - Good food child class for food that the user wants to consume"""
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

"""RYAN2 - Bad food child class for food that the user doesn't want to consume"""
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

    # sets up the game variables
    def setup(self):
        
        self.snake = snake.Snake(100, 100, 5)
        self.goodfood = GoodFood()
        self.badfood = BadFood()
        #self.background = arcade.load_texture("bg.jpg")
        self.center_window()
        """Ryan 2 - calls on food.setup method"""
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

        """Ryan 2 - Created two collission conditions, one for good food and one for bad"""        
        """Jeff - updated collision handling"""
        for seg in self.snake.snake_list:
            goodfood_collision = arcade.check_for_collision_with_list(seg, self.goodfood.food_list)
            if goodfood_collision:
                break

        for seg in self.snake.snake_list:
            badfood_collision = arcade.check_for_collision_with_list(seg, self.badfood.food_list)
            if badfood_collision:
                break

        """Ryan2 - Gives a point and resets the food items if good food is consumed"""
        for self.goodfood.food in goodfood_collision:
            self.score += 1
            """Ryan 2 - Changes food everytime one is collided"""
            self.goodfood.setup()
            self.badfood.setup()
            self.snake.grow()

        """Ryan2 - Removes bad food that is consumed, but not points"""
        for self.badfood.food in badfood_collision:
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
