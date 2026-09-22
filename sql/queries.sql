-- 1. Total amount spent
SELECT
    SUM(amount) AS total_expense
FROM expenses;


-- 2. Average expense
SELECT
    AVG(amount) AS average_expense
FROM expenses;


-- 3. Number of transactions
SELECT
    COUNT(*) AS total_transactions
FROM expenses;


-- 4. Total spending by category
SELECT
    category,
    SUM(amount) AS total_spent
FROM expenses
GROUP BY category
ORDER BY total_spent DESC;


-- 5. Spending by payment method
SELECT
    payment_method,
    SUM(amount) AS total_spent
FROM expenses
GROUP BY payment_method
ORDER BY total_spent DESC;


-- 6. Largest individual expenses
SELECT
    expense_date,
    category,
    description,
    amount,
    merchant
FROM expenses
ORDER BY amount DESC
LIMIT 10;


-- 7. Spending by merchant
SELECT
    merchant,
    SUM(amount) AS total_spent
FROM expenses
GROUP BY merchant
ORDER BY total_spent DESC;