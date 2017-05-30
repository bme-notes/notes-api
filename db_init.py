import sqlite3

db_file = "database.sqlite"
conn = sqlite3.connect(db_file)
cur = conn.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS subjects (name TEXT PRIMARY KEY, updated TEXT, url TEXT)")

conn.commit()
conn.close()
