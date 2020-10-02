import sqlite3

connection = sqlite3.connect('data.db')
cursor = connection.cursor()

user = [
    (1, 'csd1', 'csd1'),
    (2, 'csd2', 'csd2')
]
insert_query = "INSERT INTO users VALUES(?,?,?)"
cursor.executemany(insert_query, user)

connection.commit()
connection.close()
