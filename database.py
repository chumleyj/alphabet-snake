import sqlite3
import random

"""
Function: create_database
Description: Creates a the sqlite database for the words,
and then inserts the words into the database with word_id.

Function Variables:
    mycursor: stores the connection to the database.
    insert_words: stores the word_ids and words that will be
                  inserted into the database.
"""
def create_database():
    conn = sqlite3.connect('words.db')

    mycursor = conn.cursor()

    mycursor.execute("DROP TABLE IF EXISTS game_words")

    mycursor.execute("""CREATE TABLE IF NOT EXISTS game_words (
                    Id INTEGER NOT NULL PRIMARY KEY,
                    game_word TEXT NOT NULL
                    )""")

    insert_words = [
        (1, 'Airplane'),
        (2, 'Basketball'),
        (3, 'Cat'),
        (4, 'Clock'),
        (5, 'Hat'),
        (6, 'House'),
        (7, 'Pig'),
        (8, 'Table'),
        (9, 'Baseball'),
        (10, 'Car'),
        (11, 'Chair')
    ]
    mycursor.executemany("INSERT INTO game_words VALUES (?,?)", insert_words)

    conn.commit()

    conn.close()


"""
Function: get_words
Description: Selects the words from the database and stores
             them in a list of tuples.

Function Variables:
    mycursor: stores the connection to the database.
    words_list: stores the word_ids and words that are fetched
                from the database.
"""


def get_words():
    conn = sqlite3.connect('words.db')

    mycursor = conn.cursor()

    mycursor.execute("SELECT * FROM game_words")

    words_list = mycursor.fetchall()

    return words_list

"""
Function: select_word
Description: Selects a random word from the list of words
             that were fetched from the database.

Function Variables:
    game_words_list: stores the word_ids and words that are
                     fetched from the database.
    words_id: stores the random integer that is used to select
              the word from word_ids.
    game_words: stores the word_ids and words that were fetched
                from the database in a dictionary to easily compare
                the word_ids.
    selected_word: stores the word that has the id from the randomly
                   selected word_id priorly.
"""


def select_word():
    game_words_list = get_words()

    word_id = random.randrange(1, len(game_words_list)+1)

    game_words = dict(game_words_list)

    selected_word = game_words[word_id]

    return selected_word


"""

Function: total_words
Description: Is used to know the number of words that are stored in
             the database.

Function Variables:
    game_words_list: Stores the word_ids and words that are
                     fetched from the database. Is used with
                     the len() function to know the length to
                     determine the length of the list.
"""


def total_words():
    game_words_list = get_words()

    return len(game_words_list)
