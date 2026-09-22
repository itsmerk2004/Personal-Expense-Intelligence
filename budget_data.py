import sqlite3

DATABASE_FILE = "database/expenses.db"

connection = sqlite3.connect(DATABASE_FILE)
cursor = connection.cursor()

# Add monthly category budgets
budgets = [
    ("2026-09-01", "Food", 4000),
    ("2026-09-01", "Shopping", 5000),
    ("2026-09-01", "Bills", 3500),
    ("2026-09-01", "Transport", 3000),
    ("2026-09-01", "Entertainment", 2000),
    ("2026-09-01", "Health", 1500)
]

cursor.executemany("""
    INSERT INTO budgets
    (month, category, budget_amount)
    VALUES (?, ?, ?)
""", budgets)

connection.commit()
connection.close()

print("Budget data inserted successfully!")