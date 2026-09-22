import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

DATABASE_FILE = "database/expenses.db"

# Connect to database
connection = sqlite3.connect(DATABASE_FILE)

# Get category-wise spending
query = """
SELECT
    category,
    SUM(amount) AS total_spent
FROM expenses
GROUP BY category
ORDER BY total_spent DESC;
"""

df = pd.read_sql_query(query, connection)

connection.close()


# Create bar chart
plt.figure(figsize=(10, 5))

plt.bar(
    df["category"],
    df["total_spent"]
)

plt.title("Spending by Category")
plt.xlabel("Category")
plt.ylabel("Total Spending (₹)")

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()