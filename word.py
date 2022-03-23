from database import select_word

"""
Class: Word
Description: Stores information and methods for both an image and string
    representing a word. This information is manipulated and passed to the
    screen, allowing a user to spell out the word that is represented by
    the image shown on the screen.
Class Variables:
    word_name:
    word_array:
    word_index:
    word_file:
"""
class Word():
    """
    Function: init
    Description: Selects the words, selecting a word to use, creating an array from
        the word string, and identifying the corresponding image.
    """
    def __init__(self):
        self.word_name = select_word()
        self.word_array = self.word_array(self.word_name)
        self.word_index = 0
        self.word_file = "images/wordImages/" + self.word_name.lower() + ".png"
    
    """
    Function: word_array
    Description: Creates and returns an array from the string of letters that spells
        a word.
    Parameters:
        word: a string that represents a word.
    """
    def word_array(self, word):
        wordArray = [x for x in word]
        return wordArray
    
    """
    Function: current_letter
    Description: Identifies the current letter of the word based on the specified
        index.
    Parameters:
        word: a string that represents a word.
    """
    def current_letter(self):
        return self.word_array[self.word_index]
    
    """
    Function: word_length
    Description: Identifies the length of the specified word.
    """
    def word_length(self):
        return len(self.word_name)
    
    """
    Function: word_end
    Description: Identifies when the user has iterated to the end of the current
        word.
    """
    def word_end(self):
        return self.word_index == self.word_length()
