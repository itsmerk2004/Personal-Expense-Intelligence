import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

DATABASE_FILE = "database/expenses.db"

connection = sqlite3.connect(DATABASE_FILE)

query = """
SELECT
    expense_date,
    category,
    description,
    amount,
    merchant
FROM expenses
ORDER BY expense_date;
"""

df = pd.read_sql_query(query, connection)

connection.close()


# Calculate IQR
Q1 = df["amount"].quantile(0.25)
Q3 = df["amount"].quantile(0.75)

IQR = Q3 - Q1

upper_limit = Q3 + (1.5 * IQR)


# Identify anomalies
df["is_anomaly"] = df["amount"] > upper_limit


# Create chart
plt.figure(figsize=(12, 6))

normal_expenses = df[~df["is_anomaly"]]
anomaly_expenses = df[df["is_anomaly"]]

plt.scatter(
    normal_expenses["expense_date"],
    normal_expenses["amount"],
    label="Normal Expense"
)

plt.scatter(
    anomaly_expenses["expense_date"],
    anomaly_expenses["amount"],
    label="Anomaly",
    s=100
)


# Upper limit line
plt.axhline(
    upper_limit,
    linestyle="--",
    label=f"Anomaly Threshold (₹{upper_limit:.2f})"
)


plt.title("Expense Anomaly Detection")
plt.xlabel("Date")
plt.ylabel("Expense Amount (₹)")

plt.xticks(rotation=45)

plt.legend()

plt.tight_layout()

plt.show()