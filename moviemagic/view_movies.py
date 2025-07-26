import sqlite3

conn = sqlite3.connect('movies.db')
cursor = conn.cursor()

print("Tables in the database:")
tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
for t in tables:
    print(" -", t[0])

print("\nMovie records (if available):")
try:
    rows = cursor.execute("SELECT * FROM movies").fetchall()
    for row in rows:
        print(row)
except Exception as e:
    print("Error:", e)

conn.close()
