import arcade
from random import randrange, choice

# all possible letters
LETTER_OPTIONS = "abcdefghijklmnopqrstuvwxyz"
# x-axis spacing between letters
LETTER_OFFSET = 50

"""
Class: Letter
Description: Extension of the arcade Sprite class for a Letter sprite.
    The sprite is generated at a random location within the x and y coordinate
    minimums and maximums passed when creating an instance of the class.
Class Variables:
    letter_name: stores the letter this sprite represents.
    letter_file: stores the filepath to an image for the sprite.
"""
class Letter(arcade.Sprite):
    def __init__(self, letter, x_min, x_max, y_min, y_max):
        self.letter_name = letter
        self.letter_file = "Alphabet/" + letter.lower() + ".png"
        super().__init__(filename=self.letter_file, 
                         center_x=randrange(x_min, x_max), 
                         center_y=randrange(y_min, y_max))

"""
Class: GoodLetterList
Description: Extension of the arcade SpriteList class that stores Letter 
    sprites that the player is searching for. 
Class Variables:
    x_min, x_max, y_min, y_max: boundaries for where Letter sprites can
        be created.
"""
class GoodLetterList(arcade.SpriteList):
    """
    Function: init
    Description: Initializes SpriteList instance and sets boundary variables.
    """
    def __init__(self, x_min, x_max, y_min, y_max):
        super().__init__()
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

    """
    Function: setup
    Description: Creates a letter sprite and adds it to the GoodLetterList.
    Parameters:
        letter: the letter to add to the GoodLetterList as a Letter sprite
        x_min, x_max, y_min, y_max: boundaries for where Letter sprites can
            be created.
        avoid_sprite_list: a SpriteList to check against when creating Letter
            sprites to ensure there is no overlap in position of the sprites. 
    """
    def setup(self, letter, avoid_sprite_list):
        # create a Letter sprite based on letter parameter
        good_letter_sprite = Letter(letter, self.x_min, self.x_max, self.y_min, self.y_max)
        
        # check whether good_letter_sprite overlaps with sprites in the avoid_sprite_list
        sprite_overlap = arcade.check_for_collision_with_list(good_letter_sprite, avoid_sprite_list)
        
        # if sprites overlap, reposition good_letter_sprite and recheck for overlap until doesn't overlap
        while len(sprite_overlap) != 0:
            good_letter_sprite.center_x = randrange(self.x_min, self.x_max)
            good_letter_sprite.center_y = randrange(self.y_min, self.y_max)
            sprite_overlap = arcade.check_for_collision_with_list(good_letter_sprite, avoid_sprite_list)
        
        # add to GoodLetterList
        self.append(good_letter_sprite)

"""
Class: BadLetterList
Description: Extension of the arcade SpriteList class that stores Letter 
    sprites that the player wants to avoid.
Class Variables:
    x_min, x_max, y_min, y_max: boundaries for where Letter sprites can
        be created.
    letter_count: the number of Letter sprites in BadLetterList.
"""
class BadLetterList(arcade.SpriteList):
    """
    Function: init
    Description: Initializes SpriteList instance and sets boundary variables.
    """
    def __init__(self, x_min, x_max, y_min, y_max):
        super().__init__()
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
        self.letter_count = None
    
    """
    Function: setup
    Description: Creates multiple letter sprites and adds it to the BadLetterList.
        Will not create Letter sprites of the same letter.
    Parameters:
        avoid_letter: a letter that should not be added to the BadLetterList.
        bad_letter_count: the number of letter sprites to add to BadLetterList.
        avoid_list_1: a SpriteList (ex: a GoodLetterList) to check against the 
            BadLetterList to ensure there are no overlapping sprites.
        avoid_list_2: a SpriteList (ex: a SnakeList) to check against the 
            BadLetterList to ensure there are no overlapping sprites.
    """
    def setup(self, avoid_letter, bad_letter_count, avoid_list_1, avoid_list_2):
        
        # prevent exceeding max number of letters in the alphabet
        if bad_letter_count > 25:
            self.letter_count = 25
        else:
            self.letter_count = bad_letter_count
        
        # remove avoid_letter from the letter options
        letter_options = LETTER_OPTIONS.replace(avoid_letter.lower(), "")

        # add bad letters to SpriteList
        for i in range(self.letter_count):
            # select a random letter to add
            letter = choice(letter_options)
            
            # remove selected letter from the options (prevents duplicate bad letters)
            letter_options = letter_options.replace(letter, "")

            # create Letter sprite and add to SpriteList
            bad_letter = Letter(letter, self.x_min, self.x_max, self.y_min, self.y_max)
            
            # check whether bad_letter overlaps with other sprites in BadLetterList, avoid_list_1, or avoid_list_2
            bad_letter_overlap = arcade.check_for_collision_with_list(bad_letter, self)
            avoid_list_1_overlap = arcade.check_for_collision_with_list(bad_letter, avoid_list_1)
            avoid_list_2_overlap = arcade.check_for_collision_with_list(bad_letter, avoid_list_2)
            
            # if bad_letter overlaps, reposition it and recheck for overlap until doesn't overlap
            while len(bad_letter_overlap) != 0 or len(avoid_list_1_overlap) != 0 or len(avoid_list_2_overlap) != 0:
                bad_letter.center_x = randrange(self.x_min, self.x_max)
                bad_letter.center_y = randrange(self.y_min, self.y_max)
                bad_letter_overlap = arcade.check_for_collision_with_list(bad_letter, self)
                avoid_list_1_overlap = arcade.check_for_collision_with_list(bad_letter, avoid_list_1)
                avoid_list_2_overlap = arcade.check_for_collision_with_list(bad_letter, avoid_list_2)

            # add bad_letter to BadLetterList
            self.append(bad_letter)


"""
Class: CompletedLetterList
Description: Extension of the arcade SpriteList class that stores Letter 
    sprites that the player has already collected and Sprites for underscores
    equal for a provided number of letters.
Class Variables:
    num_letters: the number of letters that will be added to the 
        CompletedLetterList to complete a word.
    x_center: the x-position for the center of the first Letter sprite.
    y_center: the y-position for the center of Letter sprites.
    x_offset: the amount of offset from the first Letter sprite to the
        next one to be added in the x-axis.
"""
class CompletedLetterList(arcade.SpriteList):
    def __init__(self):
        super().__init__()
        self.num_letters = None
        self.x_center = None
        self.y_center = None
        self.x_offset = None
    
    """
    Function: setup
    Description: Creates Sprites that are underscores for each letter that
        in a word (num_letters).
    Parameters:
        num_letters: the number of letters that will eventually be in the 
            CompletedLetterList.
        center_y: the y-position for the center of Letter sprites.
        center_start_x: the x-position for the center of the first Letter and
            underscore Sprites.
    """
    def setup(self, num_letters, center_y, center_start_x):
        
        # set class variables
        self.y_center = center_y
        self.x_center = center_start_x
        self.num_letters = num_letters
        self.x_offset = 0

        # offset variable for placing underscores. Must leave x_offset unchanged
        # so that it can be used for placing Letter Sprites.
        letter_offset = 0

        # create an underscore for each letter
        for i in range(0, self.num_letters):
            new_underscore_sprite = arcade.Sprite(filename="images\white_underscore.png", 
                                                  center_x=self.x_center + letter_offset, 
                                                  center_y=self.y_center - 30)
            self.append(new_underscore_sprite)
            # offset for next underscore
            letter_offset += LETTER_OFFSET
    
    """
    Function: add_letter
    Description: Creates a Letter Sprite for a completed/found letter and adds it
        to CompletedLetterList.
    Parameters:
        completed_letter: a letter to add to the CompletedLetterList.
    """
    def add_letter(self, completed_letter):
        # create a new Letter sprite for the completed_letter
        completed_letter_sprite = Letter(completed_letter, 
                                   self.x_center + self.x_offset, 
                                   self.x_center + self.x_offset + 1, 
                                   self.y_center, 
                                   self.y_center + 1)
        
        # add completed_letter_sprite to CompletedLetterList and adjust x_offset for next letter
        self.append(completed_letter_sprite)
        self.x_offset += LETTER_OFFSET