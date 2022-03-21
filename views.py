import arcade
from database import *
import main

# Screen settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800

# Class for the starting view that will show once a user loads the game
class StartView(arcade.View):

    # Creates the resources that will be used in the StartView
    def on_show(self):
        self.background = arcade.load_texture("images/startview.jpg")
        self.yum = arcade.load_sound("sounds/yum.mp3")

    # Creates and renders the screen
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
            test_view = main.TestView()
            test_view.setup()
            self.window.show_view(test_view)    
            
# Commands while in the InstructionView
class InstructionView(arcade.View):

    # Sets values for the Instruction background and for sound effects
    def on_show(self):
        self.background = arcade.load_texture("images/instruction_screen.gif")
        self.yum = arcade.load_sound("sounds/yum.mp3")

    # Clears what was previously on the screen and fills the screen with the selected background
    def on_draw(self):
        self.clear()
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0,0,SCREEN_WIDTH,SCREEN_HEIGHT,self.background)

    # Allows users to move back to the StartView or begin gameplay
    def on_key_press(self, symbol, modifiers):
        if (symbol == arcade.key.LEFT):
            start_view = StartView()
            self.window.show_view(start_view)
        elif (symbol == arcade.key.P):
            arcade.play_sound(self.yum)
            test_view = main.TestView()
            test_view.setup()
            self.window.show_view(test_view)    

# Screen and music that starts once a player dies
class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()
        self.bg_music = arcade.load_sound("sounds/chopin_funeral_march.mp3")
        self.media_player = self.bg_music.play()
        # Background image that populates once the player dies
        self.texture = arcade.load_texture("images/game_over.jpg")

    # Clears the screen of previous content and populates the screen with the background image
    def on_draw(self):
        self.clear()
        # Populates the screen with the background image
        self.texture.draw_sized(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                                SCREEN_WIDTH, SCREEN_HEIGHT)

    # Allows the user to return to normal gameplay by clicking the screen
    def on_key_press(self, symbol, modifiers):
        # Will go to main gameplay once player presses 'P'
        if (symbol == arcade.key.P):
            test_view = main.TestView()
            self.media_player.pause()
            test_view.setup()
            self.window.show_view(test_view)
