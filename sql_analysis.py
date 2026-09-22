import sqlite3
import pandas as pd

DATABASE_FILE = "database/expenses.db"

# Connect to SQLite
connection = sqlite3.connect(DATABASE_FILE)


# 1. Total expense
query = """
SELECT SUM(amount) AS total_expense
FROM expenses;
"""

df = pd.read_sql_query(query, connection)

print("\n===== TOTAL EXPENSE =====")
print(df)


# 2. Average expense
query = """
SELECT AVG(amount) AS average_expense
FROM expenses;
"""

df = pd.read_sql_query(query, connection)

print("\n===== AVERAGE EXPENSE =====")
print(df)


# 3. Number of transactions
query = """
SELECT COUNT(*) AS total_transactions
FROM expenses;
"""

df = pd.read_sql_query(query, connection)

print("\n===== TOTAL TRANSACTIONS =====")
print(df)


# 4. Spending by category
query = """
SELECT
    category,
    SUM(amount) AS total_spent
FROM expenses
GROUP BY category
ORDER BY total_spent DESC;
"""

df = pd.read_sql_query(query, connection)

print("\n===== SPENDING BY CATEGORY =====")
print(df)

# 5. Spending by payment method
query = """
SELECT
    payment_method,
    SUM(amount) AS total_spent
FROM expenses
GROUP BY payment_method
ORDER BY total_spent DESC;
"""

df = pd.read_sql_query(query, connection)

print("\n===== SPENDING BY PAYMENT METHOD =====")
print(df)


# 6. Top 10 largest expenses
query = """
SELECT
    expense_date,
    category,
    description,
    amount,
    merchant
FROM expenses
ORDER BY amount DESC
LIMIT 10;
"""

df = pd.read_sql_query(query, connection)

print("\n===== TOP 10 LARGEST EXPENSES =====")
print(df)


# 7. Spending by merchant
query = """
SELECT
    merchant,
    SUM(amount) AS total_spent
FROM expenses
GROUP BY merchant
ORDER BY total_spent DESC;
"""

df = pd.read_sql_query(query, connection)

print("\n===== SPENDING BY MERCHANT =====")
print(df)

# 8. Daily spending
query = """
SELECT
    expense_date,
    SUM(amount) AS daily_spending
FROM expenses
GROUP BY expense_date
ORDER BY expense_date;
"""

df = pd.read_sql_query(query, connection)

print("\n===== DAILY SPENDING =====")
print(df)

# Close database connection
connection.close()