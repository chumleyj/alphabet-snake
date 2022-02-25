import arcade
from random import randrange

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800
FOOD_COUNT = 10

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