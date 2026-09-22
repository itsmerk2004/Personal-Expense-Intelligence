import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

DATABASE_FILE = "database/expenses.db"

connection = sqlite3.connect(DATABASE_FILE)

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


# Convert date to datetime
df["expense_date"] = pd.to_datetime(df["expense_date"])


# Create numerical day index
df["day_number"] = range(len(df))


# Prepare training data
X = df[["day_number"]]
y = df["daily_spending"]


# Create and train model
model = LinearRegression()
model.fit(X, y)


# Forecast next 7 days
future_days = range(
    len(df),
    len(df) + 7
)

future_df = pd.DataFrame({
    "day_number": future_days
})

future_df["forecast"] = model.predict(
    future_df[["day_number"]]
)


# Generate future dates
future_df["expense_date"] = pd.date_range(
    start=df["expense_date"].max() + pd.Timedelta(days=1),
    periods=7
)


print("\n===== EXPENSE FORECAST =====")

print(
    future_df[
        ["expense_date", "forecast"]
    ].to_string(index=False)
)


# Create visualization
plt.figure(figsize=(12, 6))

plt.plot(
    df["expense_date"],
    df["daily_spending"],
    marker="o",
    label="Actual Spending"
)

plt.plot(
    future_df["expense_date"],
    future_df["forecast"],
    marker="o",
    linestyle="--",
    label="Forecast"
)

plt.title("Daily Expense Forecast")
plt.xlabel("Date")
plt.ylabel("Spending (₹)")

plt.xticks(rotation=45)

plt.legend()

plt.tight_layout()

# Save chart
plt.savefig("expense_forecast.png", dpi=300)

plt.show()

print("\nForecast chart saved as expense_forecast.png")