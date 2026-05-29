import sqlite3

conn = sqlite3.connect('alexa.db')

cursor = conn.cursor()

cursor.execute('SELECT * FROM chats')

rows = cursor.fetchall()

for row in rows:
    print(row)