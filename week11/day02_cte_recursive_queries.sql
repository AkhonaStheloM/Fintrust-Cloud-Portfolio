-- Basic CTE: calculate account monthly totals, then filter high-value accounts
WITH monthly_totals AS (
    SELECT
        account_id,
        DATE_TRUNC('month', transaction_date) AS txn_month,
        SUM(amount)                              AS total_amount,
        COUNT(*)                                 AS txn_count
    FROM transactions
    GROUP BY account_id, DATE_TRUNC('month', transaction_date)
)
SELECT
    account_id,
    txn_month,
    total_amount
FROM monthly_totals
WHERE total_amount > 50000
ORDER BY total_amount DESC;
-- Multi-step: identify high-risk accounts via chained CTEs
WITH

-- Step 1: calculate 30-day transaction velocity per account
recent_activity AS (
    SELECT
        account_id,
        COUNT(*) AS txn_count_30d,
        SUM(amount) AS total_30d
    FROM transactions
    WHERE transaction_date >= CURRENT_DATE - INTERVAL '30 days'
    GROUP BY account_id
),

-- Step 2: get average velocity for all accounts (baseline)
avg_velocity AS (
    SELECT
        AVG(txn_count_30d) AS avg_count,
        STDDEV(txn_count_30d) AS stddev_count
    FROM recent_activity
),

-- Step 3: flag accounts more than 2 standard deviations above mean
flagged_accounts AS (
    SELECT r.account_id, r.txn_count_30d, r.total_30d
    FROM recent_activity r, avg_velocity a
    WHERE r.txn_count_30d > a.avg_count + (2 * a.stddev_count)
)

-- Final: join to account details for the alert report
SELECT f.account_id, a.customer_name, f.txn_count_30d, f.total_30d
FROM flagged_accounts f
JOIN accounts a ON f.account_id = a.account_id
ORDER BY f.txn_count_30d DESC;

-- Recursive CTE: walk an organisational hierarchy
-- (e.g. account relationships / referral chains)
WITH RECURSIVE account_hierarchy AS (

    -- Anchor: start with root accounts (no parent)
    SELECT
        account_id,
        parent_account_id,
        account_name,
        0 AS depth
    FROM accounts
    WHERE parent_account_id IS NULL

    UNION ALL

    -- Recursive member: find children of already-found accounts
    SELECT
        a.account_id,
        a.parent_account_id,
        a.account_name,
        h.depth + 1
    FROM accounts a
    JOIN account_hierarchy h ON a.parent_account_id = h.account_id
)

SELECT account_id, account_name, depth
FROM account_hierarchy
ORDER BY depth, account_name;
