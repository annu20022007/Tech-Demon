import sqlite3

conn = sqlite3.connect('test.db')
c = conn.cursor()
c.execute('SELECT id, email, hashed_password FROM users')
rows = c.fetchall()
print(rows)
