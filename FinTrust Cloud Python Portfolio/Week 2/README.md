# Week 02: Python and SQL Foundations

Week 02 develops practical foundations for analysing and processing FinTrust Bank SA transaction data. The work combines Python decision logic with SQL querying and analytical techniques that support customer reporting, transaction monitoring, and early fraud analysis.

## What I practised

- Python conditionals and functions
- Financial value formatting and compound-interest calculations
- Transaction classification and decision-engine logic
- SQL joins across customers, accounts, and transactions
- Filtering, grouping, aggregate functions, and `HAVING`
- Common table expressions (CTEs)
- Window functions, ranking, running totals, and month-to-month comparisons

## Python work

| File | Focus |
|---|---|
| `conditions.py` | Transaction classification, interest-rate selection, ATM withdrawal checks, and transaction tagging |
| `exercise1_day3.py` | Account-summary formatting, compound interest, and transaction-list calculations |
| `transaction_flowchart_day04.py` | A transaction decision engine that returns approved, pending, review, or blocked outcomes |

The Python scripts include sample calls so their behaviour can be observed directly. Run them with Python 3 from the Python folder:

```bash
python conditions.py
python exercise1_day3.py
python transaction_flowchart_day04.py
```

## SQL work

| File | Focus |
|---|---|
| `day1_joins.sql` | Customer, account, and transaction joins; filtering; and identifying customers without transactions |
| `day2_aggregates.sql` | Counts, totals, averages, grouping, monthly summaries, and a possible fraud signal |
| `day2_window_functions.sql` | Customer tiers, ranking, running totals, and month-to-month spending comparisons |

The SQL queries use the `fintrust_db` database and build on the FinTrust schema and sample data introduced in the earlier SQL portfolio work. They are written for MySQL-compatible syntax.

## FinTrust relevance

These exercises are small practice components of the wider FinTrust cloud-learning scenario. They help build the foundations needed for secure transaction processing, customer analysis, reporting, fraud monitoring, and later cloud-based data solutions.

This is a learning portfolio. The files demonstrate practice work and do not claim that a complete production banking system has been built.
