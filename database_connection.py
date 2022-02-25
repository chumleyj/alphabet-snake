import sqlite3

conn = sqlite3.connect('words.db')

mycursor = conn.cursor()

mycursor.execute("SELECT * FROM easy_words")

easy_words = mycursor.fetchall()

for word in easy_words:
    print(word)

mycursor.execute("SELECT * FROM normal_words")

normal_words = mycursor.fetchall()

for word in normal_words:
    print(word)

mycursor.execute("SELECT * FROM hard_words")

hard_words = mycursor.fetchall()

for word in hard_words:
    print(word)