import sqlite3

conn = sqlite3.connect('words.db')

mycursor = conn.cursor()

mycursor.execute("""CREATE TABLE easy_words (
                    Id INTEGER NOT NULL PRIMARY KEY,
                    easy_word TEXT NOT NULL
                )""")

insert_easy = [
                (1, 'Hat'),
                (2, 'Cat'),
                (3, 'Pig'),
                (4, 'Car'),
                (5, 'Bed'),
                (6, 'Mud'),
                (7, 'Tub'),
                (8, 'Wet'),
                (9, 'Red'),
                (10, 'Blue'),
                (11, 'Green'),
                (12, 'Boat'),
                (13, 'Tree'),
                (14, 'Sun'),
                (15, 'Cake'),
            ]
mycursor.executemany("INSERT INTO easy_words VALUES (?,?)", insert_easy)

mycursor.execute("""CREATE TABLE normal_words (
                    Id INTEGER NOT NULL PRIMARY KEY,
                    normal_word TEXT NOT NULL
                )""")

insert_normal = [
                (1, 'Clock'),
                (2, 'House'),
                (3, 'Table'),
                (4, 'Chair'),
                (5, 'Shoes'),
                (6, 'Watch'),
                (7, 'Ocean'),
                (8, 'Balloon'),
                (9, 'River'),
                (10, 'Square'),
                (11, 'Circle'),
                (12, 'Triangle'),
                (13, 'Giraffe'),
                (14, 'Crown'),
                (15, 'Pencil'),
            ]
mycursor.executemany("INSERT INTO normal_words VALUES (?,?)", insert_normal)

mycursor.execute("""CREATE TABLE hard_words (
                    Id INTEGER NOT NULL PRIMARY KEY,
                    hard_word TEXT NOT NULL
                )""")

insert_hard = [
                (1, 'Airplane'),
                (2, 'Basketball'),
                (3, 'Baseball'),
                (4, 'Football'),
                (5, 'Headlights'),
                (6, 'Vacuum'),
                (7, 'Mountain'),
                (8, 'Receipt'),
                (9, 'Earthquake'),
                (10, 'Campfire'),
                (11, 'Carousel'),
                (12, 'Fahrenheit'),
                (13, 'Celsius'),
                (14, 'Politician'),
                (15, 'Calendar'),
            ]
mycursor.executemany("INSERT INTO hard_words VALUES (?,?)", insert_hard)

conn.commit()

conn.close()