import pandas as pd
import sqlite3

# File locations
CSV_FILE = "data/expenses.csv"
DATABASE_FILE = "database/expenses.db"


# Read CSV file
df = pd.read_csv(CSV_FILE)

print("CSV data loaded successfully!")
print(f"Number of records: {len(df)}")


# Connect to SQLite database
connection = sqlite3.connect(DATABASE_FILE)


# Insert data into expenses table
df.to_sql(
    "expenses",
    connection,
    if_exists="append",
    index=False
)


connection.close()

print("Data imported into SQLite successfully!")