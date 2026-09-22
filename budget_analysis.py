import sqlite3
import pandas as pd

DATABASE_FILE = "database/expenses.db"

connection = sqlite3.connect(DATABASE_FILE)

query = """
SELECT
    b.category,
    b.budget_amount,
    COALESCE(SUM(e.amount), 0) AS actual_spending,
    b.budget_amount - COALESCE(SUM(e.amount), 0) AS remaining_budget,
    CASE
        WHEN COALESCE(SUM(e.amount), 0) > b.budget_amount
        THEN 'Over Budget'
        ELSE 'Within Budget'
    END AS status
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

print("\n===== BUDGET VS ACTUAL SPENDING =====")
print(df)