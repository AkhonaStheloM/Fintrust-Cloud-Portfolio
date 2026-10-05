# Week 04: Database Architecture and Local Transaction Analytics

Week 04 combines a proposed database architecture for FinTrust with Python source for a local CSV-to-SQLite workflow and pandas analysis. The folder also contains architecture notes, a reflection document, and a saved transaction report.

The cloud design is documentation, not a deployed system. The Python scripts currently contain syntax and indentation errors, so the saved report should not be treated as proof that this checkout runs successfully.

## Files and purposes

| File | Purpose |
| --- | --- |
| [Python/pipeline.py](Python/pipeline.py) | Defines CSV validation, SQLite table creation, transaction insertion, and summary reporting. |
| [Python/analyse.py](Python/analyse.py) | Defines pandas filtering, aggregation, enrichment, and CSV export from SQLite. |
| [Python/requirements.txt](Python/requirements.txt) | Pins pandas, NumPy, and supporting dependencies, including AWS SDK packages not used by these scripts. |
| [docs/db-architecture-diagram.md](docs/db-architecture-diagram.md) | Records the proposed seven-layer database design and DMS migration concept. |
| [docs/reflection.md](docs/reflection.md) | Discusses workload separation, SQLite versus RDS, packaging benefits, and networking considerations. |
| [reports/daily_report.txt](reports/daily_report.txt) | Contains a saved report showing eight transactions totaling ZAR 16,996.49. |

No input CSV, SQLite database, enriched CSV, packaged implementation, or automated tests are included in the supplied file inventory. The reflection’s references to `loader.py` and `database.py` describe a modular approach, not files present here.

## Intended local workflow

1. **Read and validate CSV rows.** The pipeline expects `transactions.csv` with these headers:

   ```text
   transaction_id,account_from,account_to,amount,currency,type,status,timestamp
   ```

   Validation checks for a nonempty source account, a positive numeric amount, a recognized transaction type, and a recognized status. Accepted types are `TRANSFER`, `DEPOSIT`, and `WITHDRAWAL`; accepted statuses are `COMPLETED`, `FAILED`, and `PENDING`.

2. **Load SQLite.** Valid rows are intended to enter the `transactions` table in `fintrust_analytics.db`, with a load timestamp. Transaction IDs are primary keys. The insertion code counts integrity errors as skipped rows, rather than distinguishing duplicate IDs from other constraint failures.

3. **Generate a report.** SQL queries calculate totals, breakdowns by type and status, and the three largest transactions. The intended output is `daily_report.txt` in the working directory, not automatically in `reports/`.

4. **Analyse and enrich.** The pandas script reads the table, filters completed transfers and above-average amounts, groups transaction volumes, and adds `high_value` and `txn_date` columns. Its intended export is `transactions_enriched.csv`.

Validation does not comprehensively check every field. Reporting labels amounts as ZAR without checking or converting currencies, and the “daily” report queries all stored transactions rather than filtering a particular day.

## Prerequisites and local checks

Use Python 3.11 or newer with a compatible environment for the pinned dependencies. SQLite support comes from Python’s standard library. AWS credentials are not required for these local scripts.

From the repository root, prepare an isolated environment:

```bash
cd week04/Python
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m py_compile pipeline.py analyse.py
```


**Current-code limitation:** `pipeline.py` has malformed indentation around `insert_transactions` and the main block. `analyse.py` has an unclosed `print(by_type` call. Compilation is expected to expose these problems; neither script is currently runnable as supplied.

After correcting those errors and supplying a CSV with the required headers, the intended sequence is:

```bash
python pipeline.py
python analyse.py
```

Both scripts resolve paths relative to the current working directory. The pipeline writes a local database and replaces its report output; analysis replaces its exported CSV. No successful execution is asserted here.

## Proposed AWS architecture

The diagram assigns transactions, reporting, sessions, audit records, documents, caching, and historical analytics to separate services. It also proposes AWS DMS with change data capture for migration. These are design choices, not implemented integrations or verified deployments.

Read the diagram with these qualifications:

- Its RDS-to-Aurora arrow is not evidence of a supported direct PostgreSQL read-replica configuration.
- The audit-ledger service named in the historical design should not be assumed to be available for a new deployment; current service availability needs separate validation.
- DMS with CDC can support reduced-downtime migration, but does not guarantee zero downtime.
- Availability, failover timing, performance, and costs require configuration-specific validation.

`af-south-1` remains the recorded design region. For lab discussion or any separately authorized deployment, use facilitator-approved Stockholm (`eu-north-1`) and validate the account, service availability, region, and costs first. Nothing in this folder establishes live AWS resources or runtime evidence.