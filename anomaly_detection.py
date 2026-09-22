import sqlite3
import pandas as pd

DATABASE_FILE = "database/expenses.db"

connection = sqlite3.connect(DATABASE_FILE)

query = """
SELECT
    expense_date,
    category,
    description,
    amount,
    payment_method,
    merchant
FROM expenses
ORDER BY amount DESC;
"""

df = pd.read_sql_query(query, connection)

connection.close()


# Calculate IQR
Q1 = df["amount"].quantile(0.25)
Q3 = df["amount"].quantile(0.75)

IQR = Q3 - Q1

# Define upper limit for unusual expenses
upper_limit = Q3 + (1.5 * IQR)

# Identify anomalies
df["is_anomaly"] = df["amount"] > upper_limit

anomalies = df[df["is_anomaly"] == True]


print("\n===== ANOMALY DETECTION =====")

print(f"Q1: ₹{Q1:.2f}")
print(f"Q3: ₹{Q3:.2f}")
print(f"IQR: ₹{IQR:.2f}")
print(f"Upper limit: ₹{upper_limit:.2f}")

print("\n===== UNUSUALLY LARGE EXPENSES =====")

if len(anomalies) == 0:
    print("No unusual expenses detected.")
else:
    print(anomalies.to_string(index=False))