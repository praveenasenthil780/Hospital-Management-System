import sqlite3

conn = sqlite3.connect("hospital.db")
cursor = conn.cursor()

cursor.execute("""
    INSERT OR IGNORE INTO users
    (username, password)
    VALUES (?, ?)
""", ("admin", "1234"))

conn.commit()
conn.close()

print("Admin user created successfully.")