-- 1. See all customers
USE fintrust;

SELECT * FROM customers;

-- 2. Just names and province — alphabetical by surname
SELECT first_name, last_name, province
FROM customers
ORDER BY last_name;

-- 3. All ACTIVE accounts with their balances
SELECT account_number, account_type, balance
FROM accounts
WHERE status = 'ACTIVE'
ORDER BY balance DESC;

-- 4. Which provinces are represented?
SELECT DISTINCT province
FROM customers
ORDER BY province;

-- 5. Total value across all active accounts
SELECT SUM(balance) AS total_balance
FROM accounts
WHERE status = 'ACTIVE';