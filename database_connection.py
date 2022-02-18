import mysql.connector

mydb = mysql.connector.connect(
    host='192.168.1.183',
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