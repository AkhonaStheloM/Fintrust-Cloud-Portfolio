WITH customer_spend AS (
    SELECT
        a.customer_id,
        SUM(t.amount) AS total_spend
    FROM transactions t
    JOIN accounts a
        ON t.account_id = a.account_id
    WHERE t.transaction_date >= '2024-06-01'
      AND t.transaction_date < '2024-07-01'
    GROUP BY a.customer_id
),
customer_tiers AS (
    SELECT
        customer_id,
        total_spend,
        CASE
            WHEN total_spend >= 50000 THEN 'Premium'
            WHEN total_spend >= 10000 THEN 'Standard'
            ELSE 'Basic'
        END AS spend_tier
    FROM customer_spend
)
SELECT
    customer_id,
    spend_tier,
    total_spend,
    DENSE_RANK() OVER (
        PARTITION BY spend_tier
        ORDER BY total_spend DESC
    ) AS tier_rank
FROM customer_tiers
ORDER BY spend_tier, tier_rank;

DESCRIBE accounts;
DESCRIBE transactions;

SELECT
    transaction_id,
    transaction_date,
    amount,
    SUM(amount) OVER (
        ORDER BY transaction_date
        ROWS BETWEEN UNBOUNDED PRECEDING
        AND CURRENT ROW
    ) AS running_total
FROM transactions
ORDER BY transaction_date;

WITH monthly_spend AS (
    SELECT
        a.customer_id,
        DATE_FORMAT(t.transaction_date, '%Y-%m-01') AS month_start,
        SUM(t.amount) AS total_spend
    FROM transactions t
    JOIN accounts a
        ON t.account_id = a.account_id
    GROUP BY
        a.customer_id,
        DATE_FORMAT(t.transaction_date, '%Y-%m-01')
),
spend_compare AS (
    SELECT
        customer_id,
        month_start,
        total_spend,
        LAG(total_spend) OVER (
            PARTITION BY customer_id
            ORDER BY month_start
        ) AS prev_month_spend
    FROM monthly_spend
)
SELECT
    customer_id,
    month_start AS spike_month,
    total_spend AS current_month_amount,
    prev_month_spend
FROM spend_compare
WHERE prev_month_spend IS NOT NULL
  AND total_spend > prev_month_spend * 3
ORDER BY customer_id, month_start;