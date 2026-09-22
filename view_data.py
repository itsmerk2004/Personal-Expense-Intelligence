import sqlite3
import pandas as pd

DATABASE_FILE = "database/expenses.db"

connection = sqlite3.connect(DATABASE_FILE)

query = "SELECT * FROM expenses"

df = pd.read_sql_query(query, connection)

print(df)

connection.close()