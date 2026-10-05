# Week 02: Python and SQL Development

## Overview

Week 02 builds on the FinTrust customer, account, and transaction data model. The Python work turns banking rules into reusable functions and a transaction decision engine. The SQL work connects related records and produces summaries that support transaction analysis.

## Python Work

### Account summaries, interest calculations, and transaction statistics

[exercise1_day3.py](./Python/exercise1_day3.py) contains three practical exercises:

- An account summary function that formats the customer name, account type, balance, and account status.
- A compound interest function that calculates the final amount and interest earned using the principal, annual rate, duration, and compounding frequency.
- A transaction analysis exercise that calculates the total, average, largest and smallest amounts, and the number of transactions above R5 000.

The script uses Decimal values for balances and transaction amounts. The compound interest calculation converts the principal to a float before returning rounded Decimal results.

### Conditional banking rules

[conditions.py](./Python/conditions.py) implements four functions:

| Function | What it does |
|---|---|
| classify_transaction(amount) | Classifies positive amounts as MICRO, SMALL, STANDARD, or LARGE. Zero and negative amounts return INVALID. |
| get_interest_rate(credit_score) | Selects an interest rate from four credit score bands. |
| atm_withdraw(balance, amount) | Checks for an invalid amount, the R5 000 withdrawal limit, and insufficient funds. Returns a success flag and a message. |
| tag_transaction(tx_type, merchant_category, amount) | Tags refunds, gambling transactions, routine grocery purchases, large purchases, and standard transactions. |

The file includes example print calls demonstrating different inputs and outcomes.

### Transaction decision engine

[transaction_flowchart_day04.py](./Python/transaction_flowchart_day04.py) implements assess_transaction() with five inputs: transaction ID, customer, amount, destination, and trusted device status.

The rules are evaluated in this order:

1. Block transactions to a destination in the blocked-country list.
2. Block amounts above R50 000.
3. Block zero or negative amounts.
4. For amounts above R10 000, require OTP verification on a trusted device or request review on an unrecognised device.
5. Request review for amounts above R5 000 from an unrecognised device.
6. Approve transactions that pass the checks.

The function returns a dictionary containing tx_id, customer, status, and reason. Its outcomes are BLOCKED, PENDING, REVIEW, and APPROVED. The script includes five example cases and prints the results in a table.

## SQL Work

### Joining customers, accounts, and transactions

[day1_joins.sql](./sql/day1_joins.sql) uses table aliases and INNER JOIN queries to connect customer records to accounts and transactions. The queries cover:

- Customer names, account types, and balances, sorted by balance.
- Gauteng customers with account balances above R25 000.
- Debit transactions with customer and account details.
- Customers with no transactions, identified using NOT EXISTS.
- Transactions above R10 000 for customers in Western Cape or KwaZulu-Natal.

### Aggregate reports

[day2_aggregates.sql](./sql/day2_aggregates.sql) uses COUNT, SUM, AVG, MAX, MIN, GROUP BY, and HAVING to produce banking summaries. The queries include:

- Overall transaction counts and amounts.
- Transaction counts by type.
- Transaction counts and total amounts per customer.
- Average balances by account type.
- Provinces with credit transaction totals above R100 000.
- Monthly transaction counts and total amounts.
- Customers with more than three debit transactions in one day, highlighted as a possible fraud signal rather than a confirmed fraud finding.

### Window functions and activity comparisons

[day2_window_functions.sql](./sql/day2_window_functions.sql) extends the analysis using common table expressions and window functions:

- DENSE_RANK ranks customers within Premium, Standard, and Basic amount tiers for June 2024.
- SUM OVER calculates a running transaction total ordered by transaction date.
- LAG compares each customer's monthly amount with the previous available monthly record and identifies increases greater than three times that amount.

The queries labelled as spend sum transaction amounts without filtering by transaction type. They therefore represent total recorded transaction amounts rather than debit-only expenditure.

## How the Work Fits Together

SQL provides a way to retrieve and summarise FinTrust's stored banking records. Python provides the application logic that classifies amounts, checks withdrawal rules, and assigns transaction decisions. Together, these exercises establish a foundation for later data processing and transaction monitoring work.

## Running the Files

The Python scripts use the Python standard library and can be run from the repository root:

```text
python week02/Python/exercise1_day3.py
python week02/Python/conditions.py
python week02/Python/transaction_flowchart_day04.py
```

The SQL scripts target MySQL and start with USE fintrust_db. They require the customers, accounts, and transactions tables and suitable sample data. The window function script requires a MySQL version that supports common table expressions and window functions, such as MySQL 8.0 or later.

## Architecture Diagrams

The [diagrams folder](./diagrams/README.md) contains the Week 02 compute, storage, and transaction diagrams, with an explanation below each image.
