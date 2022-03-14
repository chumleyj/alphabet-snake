import arcade
import database
import food
import snake
import word
from database import *
from time import sleep

# Defines the number of bad_food items
FOOD_COUNT = 10

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800
SCREEN_TITLE = 'Alphabet Snake'
TILE_SCALING = 0.5
SPRITE_SCALING_BOX = 0.5
FOUND_LETTER_SPACE = {
    'image_x_center': 200, 
    'letter_x_center_start': 300, 
    'y_center': 170, 
}

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
        self.completed_letters = None
        self.wall = None
        self.word_image = None
        self.current_word = None
        self.database = None
        # RYAN 3/14/2022 - Variable for how many times the snake has collided with the wrong letters
        self.badfood_counter = 0

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
        #Creates Database for Users
        self.database = database.create_database()
        
        # setup background image
        self.background = arcade.load_texture("blackboard.jpg")
        
        # create snake Sprite
        self.snake = snake.Snake(105, 295, 7)
        
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
        self.goodfood = food.GoodLetterList()
        self.badfood = food.BadLetterList()
        self.setup_letters(self.current_word.current_letter())

        # create SpriteList to display correctly found letters
        self.completed_letters = food.CompletedLetterList()
        self.completed_letters.setup(self.current_word.word_length(), FOUND_LETTER_SPACE["y_center"], FOUND_LETTER_SPACE["letter_x_center_start"])


    # setup current word image sprite
    def setup_word_image(self, filename):
        
        # create sprite for the word image
        word_image_sprite = arcade.Sprite(filename, SPRITE_SCALING_BOX)
        word_image_sprite.center_x = FOUND_LETTER_SPACE["image_x_center"]
        word_image_sprite.center_y = FOUND_LETTER_SPACE["y_center"]
        
        # add to word image SpriteList
        self.word_image.append(word_image_sprite)
    
    # setup new lists of good and bad letters
    def setup_letters(self, letter):
        
        # remove all existing letters from good and bad food
        self.goodfood.clear()
        self.badfood.clear()

        # add next letter to good letter list and other random letters to bad letter list
        self.goodfood.setup(letter, 100, SCREEN_WIDTH - 100, 300, SCREEN_HEIGHT - 50)
        self.badfood.setup(letter, FOOD_COUNT, 100, SCREEN_WIDTH - 100, 300, SCREEN_HEIGHT - 50)


    # handles drawing for background and sprites
    def on_draw(self):
        # clears previous drawing
        self.clear() 

        # draws the backgound and snake
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH , SCREEN_HEIGHT, self.background)
        
        self.snake.draw()
        self.goodfood.draw()
        self.badfood.draw()
        self.wall.draw()
        self.word_image.draw()
        self.completed_letters.draw()
        # Ryan 3/14/2022 - Making the score a bit more noticeable.
        arcade.draw_text(f'Score: {self.score}', 20, SCREEN_HEIGHT-30, arcade.csscolor.WHITE, 16, font_name='comic')


    # for game logic
    def on_update(self, delta_time):
        self.snake.update()

        """Jeff - updated collision handling"""
        for seg in self.snake.snake_list:
            goodfood_collision = arcade.check_for_collision_with_list(seg, self.goodfood)
            if goodfood_collision:
                break

        for seg in self.snake.snake_list:
            badfood_collision = arcade.check_for_collision_with_list(seg, self.badfood)
            if badfood_collision:
                break

        # Checks if the snake collides with itself
        snake_collision = arcade.check_for_collision_with_list(self.snake.snake_head, self.snake.snake_list)

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

            # if at the end of the current word, create a new word
            if self.current_word.word_end():
                
                # Increase score by 10 for the successful word
                self.score +=10

                # clear SpriteLists
                self.word_image.clear()
                self.completed_letters.clear()
                
                # create a new word
                self.current_word = word.Word()
                
                # setup the new word
                self.setup_word_image(self.current_word.word_file)

                # setup the completed letters SpriteList for the new word
                self.completed_letters.setup(self.current_word.word_length(), FOUND_LETTER_SPACE["y_center"], FOUND_LETTER_SPACE["letter_x_center_start"])

            # setup the next round of letters
            self.setup_letters(self.current_word.current_letter())

        # If the snake eats bad food, it grows, gives sound effect, and the food disappears
        for food in badfood_collision:
            self.snake.grow()
            arcade.play_sound(self.yuck)
            food.remove_from_sprite_lists()

        # If snake collides with itself, the game quits
        for seg in snake_collision:
            arcade.play_sound(self.yuck)
            """Ryan 2/24/2022 - Updated"""
            # Stops music when player dies
            self.media_player.pause()
            # Brings up Game Over screen
            view = GameOverView()
            self.window.show_view(view)

        # RYAN 3/14/2022 - If the snake collides with 5 wrong letters, ends game
        if self.badfood_counter == 5:
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

"""Ryan 3/9/2022- Updated StartView"""
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
            test_view = TestView()
            test_view.setup()
            self.window.show_view(test_view)    
            
# Commands while in the InstructionView
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
            test_view = TestView()
            test_view.setup()
            self.window.show_view(test_view)    

"""Ryan 3/10/2022 - added music for GameOverView"""
# Screen and music that starts once a player dies
class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()
        self.bg_music = arcade.load_sound("sounds/chopin_funeral_march.mp3")
        self.media_player = self.bg_music.play()
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
            test_view = TestView()
            test_view.setup()
            self.window.show_view(test_view)    

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
