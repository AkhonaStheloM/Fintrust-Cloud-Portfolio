# Week 11: SQL Analytics and Python Concurrency

Week 11 contains standalone examples for transaction analysis, concurrent I/O, and reusable Python decorators. The SQL files cover window functions, chained common table expressions (CTEs), and recursive hierarchy traversal. The Python files demonstrate asynchronous HTTP requests, threaded S3 metadata retrieval, retries, timing, and argument validation.

These files are learning examples, not an integrated data pipeline or deployed AWS application. No schema, sample dataset, dependency manifest, automated tests, deployment configuration, or runtime evidence is included.

## Files and Purpose

| File | Purpose |
| --- | --- |
| [day01_window_functions.sql](day01_window_functions.sql) | Ranks transactions within each account using `ROW_NUMBER()` and `DENSE_RANK()`, selects up to three rows per account, and queries the database version. |
| [day02_cte_recursive_queries.sql](day02_cte_recursive_queries.sql) | Calculates monthly totals, identifies unusually high transaction counts over the last 30 days, and traverses parent-child account relationships. |
| [asyncio_basics.py](asyncio_basics.py) | Uses `aiohttp`, a shared client session, and `asyncio.gather()` to collect account API responses concurrently. |
| [concurrency.py](concurrency.py) | Uses a 32-worker thread pool and Boto3 `head_object` requests to retrieve S3 object sizes. |
| [data_pipeline_decorators.py](data_pipeline_decorators.py) | Defines retry, timing, and keyword-argument type-validation decorators, with small example functions. |

## Workflow, Inputs, and Outputs

### SQL analysis

Run the window-function example against a local PostgreSQL database containing a `transactions` table with `account_id`, `transaction_date`, and `amount`. It returns the three highest-value transaction rows per account, including both ranking columns. Selection uses `row_num`, so tied amounts do not expand the result beyond three rows. Ties have no additional ordering rule.

The CTE file contains three independent queries:

1. Group transactions by account and month, returning totals above `50000`.
2. Count transactions within the last 30 days and report accounts whose counts exceed the active-account mean by more than two standard deviations.
3. Start from accounts without parents and recursively return descendants with their depth.

These queries additionally require an `accounts` table with `account_id`, `customer_name`, `parent_account_id`, and `account_name`. Outputs are database result sets, not exported files. The recursive query has no cycle detection, so use a validated, acyclic hierarchy.

### Python examples

The asynchronous example takes account identifiers and requests JSON from the hard-coded internal account API. Its result list can contain response data or exceptions because `return_exceptions=True` is enabled.

The threaded example requests metadata for three configured S3 keys, despite comments describing a larger workload. Successful results are dictionaries containing `key` and `size`, collected in completion order. Failures are printed. The timing comments are illustrative estimates, not measured results.

The decorator module demonstrates:

- Exponential-backoff retries after exceptions.
- Printed elapsed time for a successful function call.
- Runtime checks for supplied keyword arguments.
- A transaction example that returns whether an amount is positive.

## Current-Code Limitations

In `asyncio_basics.py`, `account_ids = [range(1, 1001)]` creates one list element containing a range, rather than 1,000 integer identifiers. As written, it constructs one request using that range representation. The script also lacks explicit HTTP status checking.

In `data_pipeline_decorators.py`, `fetch_from_api` is unimplemented and returns `None`; `load_data` returns an empty list without querying a database. The retry wrapper sleeps even after its final failed attempt. Type validation accepts keyword arguments only and does not enforce missing arguments itself.

Both network examples execute their workload at module level, including when imported.

## Prerequisites and Local Use

Use Python 3.10 or newer, PostgreSQL with `psql`, and a local database populated with suitable non-sensitive data. From the `week11` directory:

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install aiohttp boto3
python -m py_compile asyncio_basics.py concurrency.py data_pipeline_decorators.py
```

Compilation checks syntax only. It does not establish functional correctness or network access.

The decorator examples can be exercised locally without AWS or API access:

```bash
python -c "from data_pipeline_decorators import load_data, process_transaction; print(load_data('transactions')); print(process_transaction(account_id=1, amount=10.0))"
```

For an existing local database named `fintrust_local`, execute the read-only SQL examples with:

```bash
psql -d fintrust_local -v ON_ERROR_STOP=1 -f day01_window_functions.sql
psql -d fintrust_local -v ON_ERROR_STOP=1 -f day02_cte_recursive_queries.sql
```

Do not run the network examples without reviewing their targets. The API example requires authorized internal connectivity and its input construction needs correction before intended use. The S3 example requires approved credentials, object permissions, and validation of the account, bucket, region, and request costs. For lab activity, use facilitator-approved Stockholm configuration. These S3 requests read metadata rather than create resources, but they still contact AWS and may incur charges.