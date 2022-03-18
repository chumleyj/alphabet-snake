import sqlite3
import random


def create_database():
    conn = sqlite3.connect('words.db')

    mycursor = conn.cursor()

    mycursor.execute("DROP TABLE IF EXISTS easy_words")
    mycursor.execute("DROP TABLE IF EXISTS normal_words")
    mycursor.execute("DROP TABLE IF EXISTS hard_words")
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
        (6, 'House')
    ]
    mycursor.executemany("INSERT INTO game_words VALUES (?,?)", insert_words)

    conn.commit()

    conn.close()


def get_words():
    conn = sqlite3.connect('words.db')

    mycursor = conn.cursor()

    mycursor.execute("SELECT * FROM game_words")

    words_list = mycursor.fetchall()

    return words_list


def select_word():
    game_words_list = get_words()

    word_id = random.randrange(1, len(game_words_list)+1)

    game_words = dict(game_words_list)

    selected_word = game_words[word_id]

    return selected_word


def total_words():
    game_words_list = get_words()

    return len(game_words_list)
