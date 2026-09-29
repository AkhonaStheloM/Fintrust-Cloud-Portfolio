use fintrust;
-- Challenge 1: customers not from Gauteng or Western Cape
SELECT * FROM customers
WHERE province IN ('Gauteng', 'Western Cape');

-- Challenge 2: accounts with balance betweem R1000  and R2000 of Cheque or Savings account
SELECT * 
FROM accounts
WHERE balance BETWEEN 1000 AND 20000
	AND account_type IN ('CHEQUE', 'SAVINGS');
    
-- Challenge 3: transactions with merchant_category with 'food' or 'groceries', for amounts over R200
SELECT * FROM transactions
WHERE merchant_category LIKE ('Groceries', 'Food')
    AND amount > 200;