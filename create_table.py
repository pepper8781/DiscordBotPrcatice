import sqlite3

dbname = 'TEST.db'
conn = sqlite3.connect(dbname)

cur = conn.cursor()
 
cur.execute('''CREATE TABLE IF NOT EXISTS users (
    user_id TEXT PRIMARY KEY,
    prompt TEXT
)''')

conn.commit()
conn.close()
