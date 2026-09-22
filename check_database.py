import sqlite3

DATABASE_NAME = "database/expenses.db"

connection = sqlite3.connect(DATABASE_NAME)
cursor = connection.cursor()

print("Columns in expenses table:")

cursor.execute("PRAGMA table_info(expenses);")

columns = cursor.fetchall()

for column in columns:
    print("-", column[1])

connection.close()