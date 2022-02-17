import mysql.connector

mydb = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='password1',
    port='3306',
    database='alphabet_snake'
)

mycursor = mydb.cursor()

mycursor.execute('SELECT * FROM easy_words')

easy_words = mycursor.fetchall()

for word in easy_words:
    print(word)