# Week 03: Transaction Data Cleaning and Reporting

Week 03 extends the FinTrust learning portfolio into a small Python transaction-processing pipeline. The work focuses on turning raw CSV data into cleaner, more useful outputs for reporting and future analysis.

## What I practised

- Reading transaction records from CSV files
- Normalising dates and converting text values into usable data types
- Handling invalid rows and reporting skipped records
- Writing cleaned CSV and JSON summary outputs
- Logging pipeline activity to the console and a log file
- Building reusable validation, formatting, calculation, and reporting helpers
- Creating a standard data-directory structure for transaction and report files
- Testing utility functions with representative FinTrust examples

## Pipeline and utility files

| File | Focus |
|---|---|
| [clean_transactions.py](clean_transactions.py) | Reads raw transactions, cleans valid rows, writes clean_transactions.csv, and creates daily_summary.json |
| [clean_transaction_v2.py](clean_transaction_v2.py) | Adds structured logging, row-level error handling, date normalisation, and a more robust pipeline flow |
| [fintrust_utils.py](fintrust_utils.py) | Provides reusable helpers for Rand formatting, ID masking, validation, fees, transaction categories, summaries, and report headers |
| [test_utils.py](test_utils.py) | Exercises the shared utility functions with sample account and transaction values |
| [setup_data_dirs.py](setup_data_dirs.py) | Creates and reports on a standard FinTrust data-directory structure |
| [requirements.txt](requirements.txt) | Records the Python dependencies used across the wider learning work |

## Data and pipeline outputs

The [data](data) folder contains the sample transaction-processing inputs and outputs:

- [raw_transactions.csv](data/raw_transactions.csv) is the source transaction data.
- [clean_transactions.csv](data/clean_transactions.csv) is the cleaned CSV output.
- [daily_summary.json](data/daily_summary.json) contains summary totals for the processed records.

The [logs](logs) folder is used by the version 2 pipeline for [pipeline.log](logs/pipeline.log), which records processing events and warnings.

## Running the exercises

Run the commands from the Week 03 folder so that the relative data and logs paths resolve correctly:

```bash
python clean_transactions.py
python clean_transaction_v2.py
python test_utils.py
python setup_data_dirs.py
```

The basic scripts use Python's standard library. The dependency file is included to record the broader tools used in the portfolio's Python work.

## FinTrust relevance

Reliable transaction data is important for customer reporting, fraud monitoring, reconciliation, and downstream analytics. This week's work practises the data-quality and automation foundations needed before transaction information can be moved into a cloud-based data platform.

This is a learning portfolio. The pipeline demonstrates local practice with sample data and does not claim to be a production banking data system.
