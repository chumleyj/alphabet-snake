import arcade
import database
import food
import snake
import word
from database import *
from time import sleep

"""
Constants used in the game
"""
BAD_LETTER_COUNT = 10 # number of bad_food items to display
SCREEN_TITLE = 'Alphabet Snake'
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800
SPRITE_SCALING_BOX = 0.5 # scales wall Sprites
LETTER_SPACE = { # defines boundaries of where letters can be placed
    'x_min': 92,
    'x_max': SCREEN_WIDTH - 75,
    'y_min': 285,
    'y_max': SCREEN_HEIGHT - 40}
FOUND_LETTER_SPACE = { # defines location to display found letters
    'image_x_center': 200,
    'letter_x_center_start': 300,
    'y_center': 170}

"""
Class: GameView
Description: Extension of the arcade View class. Contains all variables
    and methods used to play the game.
"""
class GameView(arcade.View):
    """
    Function: init
    Description: Initializes View and sets class variables to
        None. Loads sounds and music.
    """
    def __init__(self):
        # call View class initializer
        super().__init__()
        self.background = None
        self.score = 0
        self.snake = None
        self.good_food = None
        self.bad_food = None
        self.completed_letters = None
        self.wall = None
        self.word_image = None
        self.current_word = None
        self.database = None
        self.completed_list = []
        self.previous_word = ""
        # Variable for how many times the snake has collided with the wrong letters
        self.bad_food_counter = 0

        # Initializes sound and music
        self.init_sounds()

    """
    Function: init_sounds
    Description: loads sounds used in the game and starts the background music
    """
    def init_sounds(self):
        self.yum = arcade.load_sound("sounds/yum.mp3")
        self.yuck = arcade.load_sound("sounds/yuck.mp3")
        self.bg_music = arcade.load_sound("sounds/bg_music.mp3")
        self.success_sound = arcade.load_sound("sounds/powerup.mp3")
        self.media_player = self.bg_music.play(loop=True)

    """
    Function: setup
    Description: sets up the game variables
    """
    def setup(self):
        # Creates Database for Users
        self.database = database.create_database()

        # setup background image
        self.background = arcade.load_texture("images/blackboard.jpg")

        # create snake Sprite
        self.snake = snake.Snake(260, 320, 15)

        # create walls
        self.wall = arcade.SpriteList()
        for x in range(95, 1200, 7):
            wall = arcade.Sprite("Alphabet\chalk2.png", SPRITE_SCALING_BOX)
            wall.center_x = x
            wall.center_y = 285
            self.wall.append(wall)

        # set current word to spell
        self.current_word = word.Word()

        # Manually create and position a word image
        self.word_image = arcade.SpriteList()
        self.setup_word_image(self.current_word.word_file)

        # create SpriteLists for correct and incorrect letters
        self.good_food = food.GoodLetterList(LETTER_SPACE['x_min'], LETTER_SPACE['x_max'], LETTER_SPACE['y_min'], LETTER_SPACE['y_max'])
        self.bad_food = food.BadLetterList(LETTER_SPACE['x_min'], LETTER_SPACE['x_max'], LETTER_SPACE['y_min'], LETTER_SPACE['y_max'])
        self.setup_letters(self.current_word.current_letter())

        # create SpriteList to display correctly found letters
        self.completed_letters = food.CompletedLetterList()
        self.completed_letters.setup(self.current_word.word_length(), FOUND_LETTER_SPACE["y_center"], FOUND_LETTER_SPACE["letter_x_center_start"])

    """
    Function: setup_word_image
    Description: creates a Sprite for an image representing the word
        the player should spell.
    Parameters: 
        filename: filename of an image used for the sprite
    """
    def setup_word_image(self, filename):

        # create sprite for the word image
        word_image_sprite = arcade.Sprite(filename, SPRITE_SCALING_BOX)
        word_image_sprite.center_x = FOUND_LETTER_SPACE["image_x_center"]
        word_image_sprite.center_y = FOUND_LETTER_SPACE["y_center"]

        # add to word image SpriteList
        self.word_image.append(word_image_sprite)

    """
    Function: setup_letters
    Description: Updates good_food and bad_food SpriteLists with new
        letters.
    Parameters:
        letter: the letter to add to good_food and to not add to bad_food.
    """
    def setup_letters(self, letter):

        # remove all existing letters from good and bad food
        self.good_food.clear()
        self.bad_food.clear()

        # add next letter to good letter list and other random letters to bad letter list
        self.good_food.setup(letter, self.snake.snake_list)
        self.bad_food.setup(letter, BAD_LETTER_COUNT, self.good_food, self.snake.snake_list)

    """
    Function: on_draw
    Description: draws the background, score, lives, and all Sprites in the game
    """
    def on_draw(self):
        # clears previous drawing
        self.clear()

        # draws the backgound and and all Sprites
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH , SCREEN_HEIGHT, self.background)
        self.snake.draw()
        self.good_food.draw()
        self.bad_food.draw()
        self.wall.draw()
        self.word_image.draw()
        self.completed_letters.draw()

        # Displays the current score and the number of remaining lives.
        arcade.draw_text(f'Lives: {5 - (self.bad_food_counter)}', 20, SCREEN_HEIGHT-20, arcade.csscolor.WHITE, 16, font_name='comic')
        arcade.draw_text(f'Score: {self.score}', 20, SCREEN_HEIGHT-40, arcade.csscolor.WHITE, 16, font_name='comic')

    """
    Function: on_update
    Description: Updates position of the snake and handles collisions between
        the snake and good_food, bad_food, itself, or the boundary of the game.
    """
    def on_update(self, delta_time):
        # update the position of the snake
        self.snake.update()

        # identify any collisions between the snake and good_food Sprites
        for seg in self.snake.snake_list:
            goodfood_collision = arcade.check_for_collision_with_list(seg, self.good_food)
            if goodfood_collision:
                break

        # If the snake eats good food, score increases, gives sound effect, and all food resets        
        for food in goodfood_collision:
            self.score += 1
            arcade.play_sound(self.yum)

            # get name of letter found and add it to completed letters
            letter_name = food.letter_name
            self.completed_letters.add_letter(letter_name)
            food.remove_from_sprite_lists()

            # increment index of current word
            self.current_word.word_index += 1

            # Checks if you've spelled all the word
            if self.current_word.word_end():
                # Add finished word to completed list
                self.completed_list.append(self.current_word.word_name)
                self.previous_word = self.current_word.word_name

                # Play success sound effect
                arcade.play_sound(self.success_sound)

                # Increase score by 10 for the successful word
                self.score += 10

                # clear SpriteLists
                self.word_image.clear()
                self.completed_letters.clear()

                # Checks if all words from DB have been completed
                if len(self.completed_list) == total_words():
                    # Clears the completed list
                    self.completed_list.clear()

                    # Makes sure the new word is not the last one completed
                    while self.current_word.word_name == self.previous_word:
                        self.current_word = word.Word()

                    # Sets up the new word
                    self.setup_word_image(self.current_word.word_file)

                    # Sets up the completed letters SpriteList for the new word
                    self.completed_letters.setup(self.current_word.word_length(), FOUND_LETTER_SPACE["y_center"],
                                                    FOUND_LETTER_SPACE["letter_x_center_start"])

                else:
                    # Makes sure the new word is not in the list of completed words
                    while self.current_word.word_name in self.completed_list:
                        self.current_word = word.Word()

                    # Sets up the new word
                    self.setup_word_image(self.current_word.word_file)

                    # Sets up the completed letters SpriteList for the new word
                    self.completed_letters.setup(self.current_word.word_length(), FOUND_LETTER_SPACE["y_center"],
                                                    FOUND_LETTER_SPACE["letter_x_center_start"])

            # Sets up the next round of letters
            self.setup_letters(self.current_word.current_letter())

        # identify any collisions between the snake and bad_food Sprites
        for seg in self.snake.snake_list:
            badfood_collision = arcade.check_for_collision_with_list(seg, self.bad_food)
            if badfood_collision:
                break

        # If the snake eats bad food, it grows, gives sound effect, and the food disappears
        for food in badfood_collision:
            self.bad_food_counter += 1
            self.snake.grow()
            arcade.play_sound(self.yuck)
            food.remove_from_sprite_lists()

        # Checks if the snake collides with itself
        snake_collision = arcade.check_for_collision_with_list(self.snake.snake_head, self.snake.snake_list)

        ### (THIS IS CLUNKY - UPDATE) ###
        # If snake collides with itself or the game boundaries, the game quits
        if len(snake_collision) > 0 or self.snake.snake_head.center_x >= LETTER_SPACE['x_max'] or self.snake.snake_head.center_x <= LETTER_SPACE['x_min'] or self.snake.snake_head.center_y >= LETTER_SPACE['y_max'] or self.snake.snake_head.center_y <= LETTER_SPACE['y_min']:
            arcade.play_sound(self.yuck)
            # Stops music when player dies
            self.media_player.pause()
            # Brings up Game Over screen
            view = GameOverView()
            self.window.show_view(view)

        # If the snake collides with 5 wrong letters, ends game
        if self.bad_food_counter == 5:
            self.media_player.pause()
            # Brings up Game Over screen
            view = GameOverView()
            self.window.show_view(view)

    """
    Function: on_key_press
    Description: Updates the movement of the snake based on keyboard input.
    Parameters:
        symbol: represents the key pressed
    """
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

"""
Class: StartView
Description: Extension of the arcade View class. Contains content
    displayed on the startup screen for the game. Also handles
    user input while on this screen.
"""
# Class for the starting view that will show once a user loads the game
class StartView(arcade.View):

    def on_show(self):
        # Creates the resources that will be used in the StartView
        self.background = arcade.load_texture("images/startview.jpg")
        self.yum = arcade.load_sound("sounds/yum.mp3")

    def on_draw(self):
        self.clear()
        # Creates the background
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0,0,SCREEN_WIDTH,SCREEN_HEIGHT,self.background)

    # Commands while in the StartView
    def on_key_press(self, symbol, modifiers):
        # Will go into the instruction screen once the player presses the right arrow key
        if (symbol == arcade.key.RIGHT):
            instruction_view = InstructionView()
            self.window.show_view(instruction_view)
        # Will go to main gameplay once player presses 'P'
        elif (symbol == arcade.key.P):
            arcade.play_sound(self.yum)
            test_view = GameView()
            test_view.setup()
            self.window.show_view(test_view)

"""
Class: InstructionView
Description: Extension of the arcade View class. Contains content
    displayed on the instruction screen for the game. Also handles
    user input while on this screen.
"""
class InstructionView(arcade.View):

    def on_show(self):
        # Sets the background color of the StartView
        self.background = arcade.load_texture("images/instruction_screen.gif")
        self.yum = arcade.load_sound("sounds/yum.mp3")

    def on_draw(self):
        self.clear()
        # Draws text on the screen
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0,0,SCREEN_WIDTH,SCREEN_HEIGHT,self.background)

    def on_key_press(self, symbol, modifiers):
        if (symbol == arcade.key.LEFT):
            start_view = StartView()
            self.window.show_view(start_view)
        elif (symbol == arcade.key.P):
            arcade.play_sound(self.yum)
            test_view = GameView()
            test_view.setup()
            self.window.show_view(test_view)

"""
Class: GameOverView
Description: Extension of the arcade View class. Contains content
    displayed when the player loses the game. Also handles
    user input while on this screen.
"""
class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()
        self.bg_music = arcade.load_sound("sounds/chopin_funeral_march.mp3")
        self.media_player = self.bg_music.play(loop=True)
        # Background image that populates once the player dies
        self.texture = arcade.load_texture("images/game_over.jpg")

    def on_draw(self):
        self.clear()
        # Populates the screen with the background image
        self.texture.draw_sized(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                                SCREEN_WIDTH, SCREEN_HEIGHT)

    # Allows the user to return to normal gameplay by clicking the screen
    def on_key_press(self, symbol, modifiers):
        # Will go to main gameplay once player presses 'P'
        if (symbol == arcade.key.P):
            self.media_player.pause()
            test_view = GameView()
            test_view.setup()
            self.window.show_view(test_view)


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.center_window()
    start_view = StartView()
    window.show_view(start_view)
    window.set_update_rate(1/20)
    arcade.run()

if __name__ == '__main__':
    main()
