import sqlite3


connection = sqlite3.connect(
    "instance/freshsip.db"
)

cursor = connection.cursor()


cursor.execute(
    "ALTER TABLE users ADD COLUMN is_active BOOLEAN NOT NULL DEFAULT 1"
)


connection.commit()

connection.close()


print("User account status added successfully.")