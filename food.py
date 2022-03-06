import arcade
from random import randrange, choice

# all possible letters
LETTER_OPTIONS = "abcdefghijklmnopqrstuvwxyz"
LETTER_OFFSET = 50

# Class for food items
class Letter(arcade.Sprite):
    def __init__(self, letter, x_min, x_max, y_min, y_max):
        self.letter_name = letter
        self.letter_file = "Alphabet/" + letter.lower() + ".png"
        super().__init__(filename=self.letter_file, 
                         center_x=randrange(x_min, x_max), 
                         center_y=randrange(y_min, y_max))

# Class for a SpriteList of good letters
class GoodLetterList(arcade.SpriteList):
    def __init__(self):
        super().__init__()
        self.x_min = None
        self.x_max = None
        self.y_min = None
        self.y_max = None
    
    # Create a Letter sprite with the good letter and add to the sprite list
    def setup(self, letter, x_min, x_max, y_min, y_max):
        # create the filename for the letter
        good_letter_sprite = Letter(letter, x_min, x_max, y_min, y_max)
        self.append(good_letter_sprite)

# Class for a SpriteList of 
class BadLetterList(arcade.SpriteList):
    def __init__(self):
        super().__init__()
        self.x_min = None
        self.x_max = None
        self.y_min = None
        self.y_max = None
        self.letter_count = None
    
    # Create a number of letter sprites equal to the bad_letter_count parameter.
    # Letter sprites are any letter other than avoid_letter. Will not duplicate
    # letters.
    def setup(self, avoid_letter, bad_letter_count, x_min, x_max, y_min, y_max):
        
        # prevent exceeding max number of letters
        if bad_letter_count > 25:
            self.letter_count = 25
        else:
            self.letter_count = bad_letter_count
        
        # remove the letter to avoid from the list of options
        letter_options = LETTER_OPTIONS.replace(avoid_letter, "")

        # add bad letters to SpriteList
        for i in range(self.letter_count):
            # select a random letter to add
            letter = choice(letter_options)
            # remove selected letter from the options (prevents duplicate bad letters)
            letter_options = letter_options.replace(letter, "")

            # create Letter sprite and add to SpriteList
            bad_letter = Letter(letter, x_min, x_max, y_min, y_max)
            self.append(bad_letter)

# Class for a completed letter list
class CompletedLetterList(arcade.SpriteList):
    def __init__(self):
        super().__init__()
        self.num_letters = None
        self.x_center = None
        self.y_center = None
        self.x_offset = None
    
    # create underscore sprites for each letter in the word
    def setup(self, num_letters, center_y, center_start_x):
        
        self.x_center = center_start_x
        self.y_center = center_y
        self.num_letters = num_letters
        self.x_offset = 0

        letter_offset = 0

        for i in range(0, self.num_letters):
            new_underscore_sprite = arcade.Sprite(filename="images\white_underscore.png", 
                                           center_x=self.x_center + letter_offset, 
                                           center_y=self.y_center - 30)
            self.append(new_underscore_sprite)
            letter_offset += LETTER_OFFSET
    
    # add a new letter to the SpriteList
    def add_letter(self, completed_letter):
        new_letter_sprite = Letter(completed_letter, 
                                   self.x_center + self.x_offset, 
                                   self.x_center + self.x_offset + 1, 
                                   self.y_center, 
                                   self.y_center + 1)
        self.append(new_letter_sprite)
        self.x_offset += LETTER_OFFSET