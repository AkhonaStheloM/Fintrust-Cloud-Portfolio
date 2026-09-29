USE fintrust;

-- Find all customers from Gauteng
SELECT *
FROM customers
WHERE province = 'Gauteng';

-- Find all accounts with a balance greater than R5,000.
SELECT *
FROM accounts
WHERE balance > 5000;

SELECT *
FROM transactions
WHERE amount < 500;

SELECT *
FROM accounts
WHERE account_type != 'SAVINGS';

SELECT *
FROM customers
WHERE email LIKE '%gmail%';

SELECT *
FROM accounts
WHERE account_number LIKE 'FT-SAV%';

SELECT *
FROM customers
WHERE email LIKE '%.co.za';

SELECT *
FROM customers
WHERE province IN ('Gauteng','Western Cape');

SELECT *
FROM transactions
WHERE amount BETWEEN 100 AND 1000;

SELECT *
FROM transactions
WHERE merchant_category IS NULL;

SELECT *
FROM transactions
WHERE merchant_category IS NOT NULL;

SELECT *
FROM accounts
WHERE account_type = 'SAVINGS'
AND balance > 5000;

SELECT *
FROM customers
WHERE province = 'Gauteng'
OR province = 'Western Cape';

SELECT *
FROM transactions
WHERE NOT transaction_type = 'CREDIT';

SELECT *
FROM transactions
WHERE transaction_type != 'CREDIT';

SELECT *
FROM customers
WHERE province = 'Gauteng';

SELECT *
FROM accounts
WHERE balance > 5000;

-- Find all customers whose email address ends in '.co.za'.
SELECT *
FROM customers
WHERE email LIKE '%.co.za';

-- Find all transactions of type DEBIT or PAYMENT (using IN, not multiple ORs).
SELECT *
FROM transactions
WHERE transaction_type IN ('DEBIT','PAYMENT');

-- Find all SAVINGS accounts with a balance between R1,000 and R50,000.
SELECT *
FROM accounts
WHERE account_type = 'SAVINGS'
AND balance BETWEEN 1000 AND 50000;

-- Find all transactions that DO have a merchant_category recorded (not NULL).
SELECT *
FROM transactions
WHERE merchant_category IS NOT NULL;

SELECT account_id, account_number, account_type, balance
FROM accounts
WHERE balance > 10000
ORDER BY balance DESC;

SELECT account_id, customer_id, account_number, balance
FROM accounts
WHERE account_type = 'SAVINGS'
ORDER BY balance DESC;

SELECT transaction_id, account_id, amount, transaction_type, transaction_date
FROM transactions
WHERE merchant_category = 'Groceries'
AND amount > 500
ORDER BY amount DESC;

SELECT first_name, last_name, email
FROM customers
WHERE email LIKE '%gmail%'
ORDER BY last_name;

SELECT *
FROM customers
WHERE province = 'Gauteng'
AND email LIKE '%gmail%';

