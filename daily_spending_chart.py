import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

DATABASE_FILE = "database/expenses.db"

# Connect to database
connection = sqlite3.connect(DATABASE_FILE)

# Get daily spending
query = """
SELECT
    expense_date,
    SUM(amount) AS daily_spending
FROM expenses
GROUP BY expense_date
ORDER BY expense_date;
"""

df = pd.read_sql_query(query, connection)

connection.close()


# Convert date column to datetime
df["expense_date"] = pd.to_datetime(df["expense_date"])


# Create chart
plt.figure(figsize=(10, 5))

plt.plot(
    df["expense_date"],
    df["daily_spending"],
    marker="o"
)

plt.title("Daily Expense Trend")
plt.xlabel("Date")
plt.ylabel("Spending (₹)")

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()