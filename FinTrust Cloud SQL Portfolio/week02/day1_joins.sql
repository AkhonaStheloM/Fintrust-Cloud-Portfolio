USE fintrust_db;

SELECT
    c.first_name,
    c.last_name,
    a.account_type,
    a.balance
FROM customers c
INNER JOIN accounts a
    ON c.customer_id = a.customer_id
ORDER BY a.balance DESC;

-- Exercise 2: Gauteng customers with balances
SELECT
    c.first_name,
    c.last_name,
    c.province,
    a.account_type,
    a.balance
FROM customers c
INNER JOIN accounts a
    ON c.customer_id = a.customer_id
WHERE c.province = 'Gauteng'
  AND a.balance > 25000
ORDER BY a.balance DESC;

-- Exercise 3: Debit transactions
SELECT
    c.first_name,
    c.last_name,
    a.account_type,
    t.amount,
    t.transaction_date
FROM customers c
INNER JOIN accounts a
    ON c.customer_id = a.customer_id
INNER JOIN transactions t
    ON a.account_id = t.account_id
WHERE t.transaction_type = 'DEBIT'
ORDER BY t.transaction_date DESC;

-- Exercise 4: Customers with no transactions
SELECT
    c.customer_id,
    c.first_name,
    c.last_name
FROM customers c
WHERE NOT EXISTS (
    SELECT 1
    FROM accounts a
    INNER JOIN transactions t
        ON a.account_id = t.account_id
    WHERE a.customer_id = c.customer_id
);

-- Exercise 5: Transactions greater than
SELECT
    c.first_name,
    c.last_name,
    c.province,
    t.amount
FROM customers c
INNER JOIN accounts a
    ON c.customer_id = a.customer_id
INNER JOIN transactions t
    ON a.account_id = t.account_id
WHERE t.amount > 10000
  AND c.province IN ('Western Cape', 'KwaZulu-Natal')
ORDER BY t.amount DESC;

SHOW DATABASES;
SHOW TABLES;
