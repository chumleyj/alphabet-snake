from database import *

class Word():
    def __init__(self):
        self.word_name = select_word()
        self.word_array = self.word_array(self.word_name)
        self.word_index = 0
        self.word_file = "images/wordImages/" + self.word_name.lower() + ".png"

    def word_array(self, word):
        wordArray = [x for x in word]

        return wordArray

    def current_letter(self):
        return self.word_array[self.word_index]

    def word_length(self):
        return len(self.word_name)

    def word_end(self):
        if self.word_index == self.word_length():
            return True
        else:
            return False
