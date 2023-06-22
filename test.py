import sqlite3 as sql

db = sql.connect('test.db')

cursor = db.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS users (discordid TEXT, robloxid TEXT, username TEXT)''')               
cursor.execute('''INSERT INTO users VALUES ('123456789', '987654321', 'TheSkout001')''')
cursor.execute('''SELECT * FROM users''')
rows = cursor.fetchall()
for row in rows:
    print(row)
db.commit()

