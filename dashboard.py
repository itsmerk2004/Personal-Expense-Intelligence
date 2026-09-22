import sqlite3
import pandas as pd
import streamlit as st

from pathlib import Path

from data_processor import (
    map_columns,
    validate_expense_data,
    clean_expense_data
)

# --------------------------------------------------
# Load Custom CSS
# --------------------------------------------------

css_file = Path("style.css")

with open(css_file, "r", encoding="utf-8") as file:
    st.markdown(
        f"<style>{file.read()}</style>",
        unsafe_allow_html=True
    )

DATABASE_FILE = "database/expenses.db"

st.set_page_config(
    page_title="Personal Expense Intelligence",
    page_icon="💰",
    layout="wide"
)

connection = sqlite3.connect(DATABASE_FILE)

# CSV Upload
# --------------------------------------------------

uploaded_file = st.sidebar.file_uploader(
    "📂 Upload Expense CSV",
    type=["csv"]
)

if uploaded_file is not None:

    uploaded_expenses = pd.read_csv(
        uploaded_file
    )
    uploaded_expenses = map_columns(
        uploaded_expenses
    )

    is_valid, missing_columns = validate_expense_data(
        uploaded_expenses
    )

    if not is_valid:

        st.error(
            "Uploaded CSV is missing these required columns: "
            + ", ".join(missing_columns)
        )

        st.stop()

    uploaded_expenses = clean_expense_data(
        uploaded_expenses
    )

    st.sidebar.success(
        "CSV uploaded and processed successfully!"
    )

expenses = pd.read_sql_query(
    "SELECT * FROM expenses",
    connection
)

expenses["expense_date"] = pd.to_datetime(
    expenses["expense_date"]
)

if uploaded_file is not None:

    expenses = uploaded_expenses.copy()

    expenses["expense_date"] = pd.to_datetime(
        expenses["expense_date"],
        errors="coerce"
    )

    expenses["amount"] = pd.to_numeric(
        expenses["amount"],
        errors="coerce"
    )

category_query = """
SELECT
    category,
    SUM(amount) AS total_spent
FROM expenses
GROUP BY category
ORDER BY total_spent DESC;
"""

category_data = pd.read_sql_query(
    category_query,
    connection
)

payment_query = """
SELECT
    payment_method,
    SUM(amount) AS total_spent
FROM expenses
GROUP BY payment_method
ORDER BY total_spent DESC;
"""

payment_data = pd.read_sql_query(
    payment_query,
    connection
)

budget_query = """
SELECT
    b.category,
    b.budget_amount,
    COALESCE(SUM(e.amount), 0) AS actual_spending,
    b.budget_amount - COALESCE(SUM(e.amount), 0) AS remaining_budget
FROM budgets b
LEFT JOIN expenses e
    ON b.category = e.category
    AND strftime('%Y-%m', e.expense_date)
        = strftime('%Y-%m', b.month)
GROUP BY
    b.category,
    b.budget_amount
ORDER BY actual_spending DESC;
"""

budget_data = pd.read_sql_query(
    budget_query,
    connection
)

connection.close()


# --------------------------------------------------
# Anomaly detection
# --------------------------------------------------

Q1 = expenses["amount"].quantile(0.25)

Q3 = expenses["amount"].quantile(0.75)

IQR = Q3 - Q1

upper_limit = Q3 + (1.5 * IQR)

expenses["is_anomaly"] = (
    expenses["amount"] > upper_limit
)

anomalies = expenses[
    expenses["is_anomaly"]
].copy()


# --------------------------------------------------
# Dashboard title
# --------------------------------------------------
# --------------------------------------------------

st.title("💰 Personal Expense Intelligence")

st.markdown(
    """
    **Personal finance analytics dashboard** 

    Analyze spending patterns, category-wise expenses, payment methods,
    budgets, and daily spending trends.
    """
)

st.caption(
    f"Analysis period: {expenses['expense_date'].min().strftime('%d %b %Y')} "
    f"to {expenses['expense_date'].max().strftime('%d %b %Y')}"
)

# --------------------------------------------------
# Expense Filters
# --------------------------------------------------
st.sidebar.title("🔎 Filters")

categories = [
    "All Categories"
] + sorted(
    expenses["category"].unique().tolist()
)

def reset_filters():
    st.session_state["category_filter"] = "All Categories"
    st.session_state["date_filter"] = (min_date, max_date)

selected_category = st.sidebar.selectbox(
    "Select Category",
    categories,
    key="category_filter"
)


expenses["expense_date"] = pd.to_datetime(
    expenses["expense_date"]
)

min_date = expenses["expense_date"].min().date()
max_date = expenses["expense_date"].max().date()

selected_dates = st.sidebar.date_input(
    "Select Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
    key="date_filter"
)

st.sidebar.button(
    "🔄 Reset Filters",
    on_click=reset_filters
)

if selected_category == "All Categories":
    filtered_expenses = expenses.copy()
else:
    filtered_expenses = expenses[
        expenses["category"] == selected_category
    ].copy()

if len(selected_dates) == 2:

    start_date = pd.Timestamp(selected_dates[0])
    end_date = pd.Timestamp(selected_dates[1])

    filtered_expenses = filtered_expenses[
        (filtered_expenses["expense_date"] >= start_date)
        &
        (filtered_expenses["expense_date"] <= end_date)
    ]

# --------------------------------------------------
# KPI calculations
# --------------------------------------------------
st.write(
    f"Showing {len(filtered_expenses)} transaction(s)"
)

total_expense = filtered_expenses["amount"].sum()

average_expense = filtered_expenses["amount"].mean()

total_transactions = len(filtered_expenses)

highest_expense = (
    filtered_expenses["amount"].max()
    if len(filtered_expenses) > 0
    else 0
)
# --------------------------------------------------
# KPI cards
# --------------------------------------------------

col1, col2, col3, col4 = st.columns(4)


col1.metric(
    "Total Expense",
    f"₹{total_expense:,.0f}"
)


col2.metric(
    "Average Expense",
    f"₹{average_expense:,.0f}"
)


col3.metric(
    "Transactions",
    total_transactions
)


col4.metric(
    "Largest Expense",
    f"₹{highest_expense:,.0f}"
)


st.divider()

# --------------------------------------------------
# Key Insights
# --------------------------------------------------

st.subheader("💡 Key Insights")

if len(filtered_expenses) > 0:

    highest_category = (
        filtered_expenses
        .groupby("category")["amount"]
        .sum()
        .idxmax()
    )

    highest_category_amount = (
        filtered_expenses
        .groupby("category")["amount"]
        .sum()
        .max()
    )

    highest_expense_row = filtered_expenses.loc[
        filtered_expenses["amount"].idxmax()
    ]

    insight_col1, insight_col2, insight_col3 = st.columns(3)

    insight_col1.info(
        f"**Highest Spending Category**\n\n"
        f"{highest_category} — ₹{highest_category_amount:,.0f}"
    )

    insight_col2.info(
        f"**Largest Transaction**\n\n"
        f"{highest_expense_row['description']} — "
        f"₹{highest_expense_row['amount']:,.0f}"
    )

    insight_col3.info(
        f"**Filtered Spending**\n\n"
        f"₹{total_expense:,.0f} across "
        f"{total_transactions} transaction(s)"
    )

else:

    st.info("No transactions match the selected filters.")

# --------------------------------------------------
# Spending analysis
# --------------------------------------------------

col1, col2 = st.columns(2)


with col1:

    st.subheader("Spending by Category")

    filtered_category_data = (
    filtered_expenses
    .groupby("category")["amount"]
    .sum()
    .reset_index(name="total_spent")
)

st.bar_chart(
    filtered_category_data.set_index("category")
)


with col2:

    st.subheader("Spending by Payment Method")

    st.bar_chart(
        payment_data.set_index("payment_method")
    )


st.divider()


# --------------------------------------------------
# Budget analysis
# --------------------------------------------------

st.subheader("Budget vs Actual Spending")


budget_chart_data = budget_data[
    [
        "category",
        "budget_amount",
        "actual_spending"
    ]
].set_index("category")


st.bar_chart(
    budget_chart_data
)


st.subheader("Budget Details")


st.dataframe(
    budget_data,
    use_container_width=True
)


st.divider()


# --------------------------------------------------
# Anomaly detection section
# --------------------------------------------------

st.subheader("🚨 Unusual Expenses")


st.write(
    f"Expenses above ₹{upper_limit:,.2f} "
    "are classified as unusual using the IQR method."
)


if len(anomalies) == 0:

    st.success(
        "No unusual expenses detected."
    )

else:

    st.warning(
        f"{len(anomalies)} unusual expense(s) detected."
    )

    anomaly_display = anomalies[
        [
            "expense_date",
            "category",
            "description",
            "amount",
            "payment_method",
            "merchant"
        ]
    ].sort_values(
        "amount",
        ascending=False
    )

    st.dataframe(
        anomaly_display,
        use_container_width=True
    )


st.divider()


# --------------------------------------------------
# Daily Spending Trend
# --------------------------------------------------

st.divider()

st.subheader("📈 Daily Spending Trend")

daily_spending = (
    filtered_expenses
    .groupby("expense_date")["amount"]
    .sum()
    .reset_index(name="daily_spending")
)

daily_spending = daily_spending.sort_values("expense_date")

st.line_chart(
    daily_spending.set_index("expense_date")
)

# --------------------------------------------------
# Expense transactions
# --------------------------------------------------

st.subheader("Expense Transactions")


expense_display = filtered_expenses[
    [
        "expense_date",
        "category",
        "description",
        "amount",
        "payment_method",
        "merchant"
    ]
].sort_values(
    "expense_date",
    ascending=False
)


st.dataframe(
    expense_display,
    use_container_width=True
)

csv_data = filtered_expenses.to_csv(
    index=False
)

st.download_button(
    label="⬇️ Download Filtered Expenses",
    data=csv_data,
    file_name="filtered_expenses.csv",
    mime="text/csv"
)
# --------------------------------------------------
# Expense Forecast
# --------------------------------------------------

st.divider()

st.subheader("🔮 7-Day Expense Forecast")

# Prepare daily spending data
forecast_query = """
SELECT
    expense_date,
    SUM(amount) AS daily_spending
FROM expenses
GROUP BY expense_date
ORDER BY expense_date;
"""

forecast_data = pd.read_sql_query(
    forecast_query,
    sqlite3.connect(DATABASE_FILE)
)

forecast_data["expense_date"] = pd.to_datetime(
    forecast_data["expense_date"]
)

# Create numerical day index
forecast_data["day_number"] = range(
    len(forecast_data)
)

# Train linear regression model
from sklearn.linear_model import LinearRegression

X = forecast_data[["day_number"]]

y = forecast_data["daily_spending"]

model = LinearRegression()

model.fit(X, y)


# Generate next 7 days
future_days = range(
    len(forecast_data),
    len(forecast_data) + 7
)

future_data = pd.DataFrame({
    "day_number": future_days
})

future_data["forecast"] = model.predict(
    future_data[["day_number"]]
)

future_data["expense_date"] = pd.date_range(
    start=forecast_data["expense_date"].max()
    + pd.Timedelta(days=1),
    periods=7
)


# Display forecast table
st.write("Predicted daily spending:")

forecast_display = future_data[
    [
        "expense_date",
        "forecast"
    ]
].copy()

forecast_display["forecast"] = (
    forecast_display["forecast"]
    .round(2)
)

st.dataframe(
    forecast_display,
    use_container_width=True
)



# Forecast chart
st.line_chart(
    future_data.set_index("expense_date")[
        ["forecast"]
    ]
)

st.caption(
    "Forecast generated using a simple linear regression "
    "model based on historical daily spending."
)