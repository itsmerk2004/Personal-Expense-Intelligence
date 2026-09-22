import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

DATABASE_FILE = "database/expenses.db"

connection = sqlite3.connect(DATABASE_FILE)

query = """
SELECT
    b.category,
    b.budget_amount,
    COALESCE(SUM(e.amount), 0) AS actual_spending
FROM budgets b
LEFT JOIN expenses e
    ON b.category = e.category
    AND strftime('%Y-%m', e.expense_date) = strftime('%Y-%m', b.month)
GROUP BY
    b.category,
    b.budget_amount
ORDER BY actual_spending DESC;
"""

df = pd.read_sql_query(query, connection)

connection.close()


# Create chart
plt.figure(figsize=(10, 6))

x = range(len(df))

plt.bar(
    [i - 0.2 for i in x],
    df["budget_amount"],
    width=0.4,
    label="Budget"
)

plt.bar(
    [i + 0.2 for i in x],
    df["actual_spending"],
    width=0.4,
    label="Actual Spending"
)

plt.xticks(x, df["category"], rotation=45)

plt.title("Budget vs Actual Spending")
plt.xlabel("Category")
plt.ylabel("Amount (₹)")

plt.legend()

plt.tight_layout()

plt.show()