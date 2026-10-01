WITH ranked_transactions AS (
    SELECT
        account_id,
        transaction_date,
        amount,

        ROW_NUMBER() OVER (
            PARTITION BY account_id
            ORDER BY amount DESC
        ) AS row_num,

        DENSE_RANK() OVER (
            PARTITION BY account_id
            ORDER BY amount DESC
        ) AS dense_rank_num

    FROM transactions
)

SELECT *
FROM ranked_transactions
WHERE row_num <= 3
ORDER BY account_id, amount DESC;
SELECT VERSION();