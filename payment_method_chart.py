import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

DATABASE_FILE = "database/expenses.db"

# Connect to database
connection = sqlite3.connect(DATABASE_FILE)

# Get spending by payment method
query = """
SELECT
    payment_method,
    SUM(amount) AS total_spent
FROM expenses
GROUP BY payment_method
ORDER BY total_spent DESC;
"""

df = pd.read_sql_query(query, connection)

connection.close()


# Create bar chart
plt.figure(figsize=(8, 5))

plt.bar(
    df["payment_method"],
    df["total_spent"]
)

plt.title("Spending by Payment Method")
plt.xlabel("Payment Method")
plt.ylabel("Total Spending (₹)")

plt.tight_layout()

plt.show()