USE fintrust_db;

SELECT COUNT(*) AS total_transactions
FROM transactions;

SELECT SUM(amount) AS total_amount
FROM transactions;

SELECT AVG(balance) AS average_balance
FROM accounts;

SELECT MAX(amount) AS largest_transaction
FROM transactions;

SELECT MIN(amount) AS smallest_transaction
FROM transactions;

SELECT COUNT(*)
FROM transactions;

SELECT
    transaction_type,
    COUNT(*) AS total
FROM transactions
GROUP BY transaction_type;

SELECT
    transaction_type,
    COUNT(*) AS total
FROM transactions
GROUP BY transaction_type
HAVING COUNT(*) > 2;


-- Exercise 1: Transaction summary per customer
SELECT
    c.first_name,
    c.last_name,
    c.province,
    COUNT(t.transaction_id) AS total_transactions,
    SUM(t.amount) AS total_amount
FROM customers c
INNER JOIN accounts a
    ON c.customer_id = a.customer_id
INNER JOIN transactions t
    ON a.account_id = t.account_id
GROUP BY
    c.customer_id,
    c.first_name,
    c.last_name,
    c.province
HAVING COUNT(t.transaction_id) > 0
ORDER BY total_amount DESC;

-- Exercise 2: Average balance by account type
SELECT
    account_type,
    COUNT(*) AS account_count,
    AVG(balance) AS average_balance
FROM accounts
GROUP BY account_type
ORDER BY average_balance DESC;

-- Exercise 3: Provinces with deposits over R100000
SELECT
    c.province,
    SUM(t.amount) AS total_deposits,
    COUNT(t.transaction_id) AS credit_count
FROM customers c
INNER JOIN accounts a
    ON c.customer_id = a.customer_id
INNER JOIN transactions t
    ON a.account_id = t.account_id
WHERE t.transaction_type = 'CREDIT'
GROUP BY c.province
HAVING SUM(t.amount) > 100000
ORDER BY total_deposits DESC;

-- Exercise 4: Monthly transaction summary
SELECT
    YEAR(transaction_date) AS year,
    MONTH(transaction_date) AS month,
    COUNT(*) AS transaction_count,
    SUM(amount) AS total_amount
FROM transactions
GROUP BY
    YEAR(transaction_date),
    MONTH(transaction_date)
ORDER BY year, month;

-- Exercise 5: Possible fraud signal
SELECT
    c.first_name,
    c.last_name,
    DATE(t.transaction_date) AS transaction_day,
    COUNT(*) AS debit_count
FROM customers c
INNER JOIN accounts a
    ON c.customer_id = a.customer_id
INNER JOIN transactions t
    ON a.account_id = t.account_id
WHERE t.transaction_type = 'DEBIT'
GROUP BY
    c.customer_id,
    c.first_name,
    c.last_name,
    DATE(t.transaction_date)
HAVING COUNT(*) > 3
ORDER BY debit_count DESC, transaction_day;

