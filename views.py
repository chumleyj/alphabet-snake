import arcade
from database import *
import main

# Screen settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800

"""
Class: StartView
Description: Class to create a starting view that will appear on the 
screen when a user first starts the game.
Class Variables:
    background: An image that will populate the screen when a user first
    starts a game.
    yum: A sound effect that plays when the user conducts certain positive
    activities.
    instruction_view: An instance of the view that provides instructions to
    players.
    test_view: An instance of the view in which users are able to play the 
    actual game.
"""
class StartView(arcade.View):
    """
    Function: on_show
    Description: Creates the resources that will be used in the StartView.
    """
    def on_show(self):
        self.background = arcade.load_texture("images/startview.jpg")
        self.yum = arcade.load_sound("sounds/yum.mp3")
    """
    Function: on_draw
    Description: Creates and renders the screen.
    """
    def on_draw(self):
        self.clear()
        # Creates the background
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0,0,SCREEN_WIDTH,SCREEN_HEIGHT,self.background)
    """
    Function: on_key_press
    Description: Allows the user to interact with the the game through various keys.
    Parameters:
        symbol: a key that is pressed by the user to interact with the game.
    """
    def on_key_press(self, symbol, modifiers):
        # Will go into the instruction screen once the player presses the right arrow key
        if (symbol == arcade.key.RIGHT):
            instruction_view = InstructionView()
            self.window.show_view(instruction_view)    
        # Will go to main gameplay once player presses 'P'
        elif (symbol == arcade.key.P):
            arcade.play_sound(self.yum)
            test_view = main.GameView()
            test_view.setup()
            self.window.show_view(test_view)    
            
"""
Class: InstructionView
Description: Class to create an instructional view that will appear on the 
screen and provide basic gameplay directives and instructions to users.
Class Variables:
    background: An image that will populate the screen when a user first
    starts a game.
    yum: A sound effect that plays when the user conducts certain positive
    activities.
    start_view: An instance of the view that appears when a user first starts
    the program.
    test_view: An instance of the view in which users are able to play the 
    actual game.
"""
class InstructionView(arcade.View):
    """
    Function: on_show
    Description: Creates the resources that will be used in the StartView.
    """
    def on_show(self):
        self.background = arcade.load_texture("images/instruction_screen.gif")
        self.yum = arcade.load_sound("sounds/yum.mp3")
    """
    Function: on_draw
    Description: Creates and renders the screen.
    """
    def on_draw(self):
        self.clear()
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0,0,SCREEN_WIDTH,SCREEN_HEIGHT,self.background)
    """
    Function: on_key_press
    Description: Allows the user to interact with the the game through various keys.
    Parameters:
        symbol: a key that is pressed by the user to interact with the game.
    """
    def on_key_press(self, symbol, modifiers):
        if (symbol == arcade.key.LEFT):
            start_view = StartView()
            self.window.show_view(start_view)
        elif (symbol == arcade.key.P):
            arcade.play_sound(self.yum)
            test_view = main.GameView()
            test_view.setup()
            self.window.show_view(test_view)    

"""
Class: GameOverView
Description: Class to create a view that shows when the user player dies
in the game.
Class Variables:
    background: An image that will populate the screen when the GameOverView
    is displayed.
    bg_music: Contains the background music that plays while in the GamOverView.
    media_player: Plays the background music while the user is in the 
    GameOverView.
    test_view: An instance of the view in which users are able to play the 
    actual game.
"""
class GameOverView(arcade.View):
    """
    Function: init
    Description: Initializes the background textures and music.
    """
    def __init__(self):
        super().__init__()
        self.bg_music = arcade.load_sound("sounds/chopin_funeral_march.mp3")
        self.media_player = self.bg_music.play(loop=True)
        # Background image that populates once the player dies
        self.texture = arcade.load_texture("images/game_over.jpg")
    """
    Function: on_draw
    Description: Creates and renders the screen.
    """
    def on_draw(self):
        self.clear()
        # Populates the screen with the background image
        self.texture.draw_sized(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                                SCREEN_WIDTH, SCREEN_HEIGHT)
    """
    Function: on_key_press
    Description: Allows the user to interact with the the game through various keys.
    Parameters:
        symbol: a key that is pressed by the user to interact with the game.
    """
    def on_key_press(self, symbol, modifiers):
        # Will go to main gameplay once player presses 'P'
        if (symbol == arcade.key.P):
            test_view = main.GameView()
            self.media_player.pause()
            test_view.setup()
            self.window.show_view(test_view)
