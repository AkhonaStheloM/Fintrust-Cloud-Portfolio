# Week 03: Python Transaction Processing and Data Pipelines

## Overview

Week 03 develops FinTrust's transaction processing work into reusable Python modules and file-based pipelines. The work covers functions, CSV and JSON handling, directory management, exception handling, logging, and automated tests.

The main workflow reads raw transaction records, standardises their fields, writes a clean CSV file, and produces a summary of deposits and withdrawals.

## Project Files

| File | Purpose |
|---|---|
| [fintrust_utils.py](./Python/fintrust_utils.py) | Reusable formatting, validation, calculation, and reporting functions. |
| [setup_data_dirs.py](./Python/setup_data_dirs.py) | Creates a structured data directory and reports its contents. |
| [clean_transactions.py](./Python/clean_transactions.py) | Cleans transaction records and generates CSV and JSON outputs. |
| [clean_transaction_v2.py](./Python/clean_transaction_v2.py) | Adds logging, row numbers, skipped-row counts, and input-file checks to the pipeline. |
| [test_utils.py](./Python/test_utils.py) | Unit tests for the banking utility functions. |
| [test_pipeline.py](./Python/test_pipeline.py) | Helper tests and integration tests for transaction processing. |
| [requirements.txt](./Python/requirements.txt) | Lists boto3, pandas, and python-dotenv dependencies. |
| [.gitignore](./Python/.gitignore) | Excludes virtual environments, environment files, Python cache, and editor files. |

## Reusable Banking Utilities

The fintrust_utils module separates common banking operations into functions that can be reused by other scripts:

- Format amounts as South African Rand.
- Mask the middle six digits of a 13-digit ID string.
- Check that an ID contains 13 numeric characters.
- Validate cheque, savings, and credit account types.
- Calculate simple interest for a period expressed in months.
- Select monthly fees by account type.
- Categorise transactions as small, medium, or large using the absolute amount.
- Summarise positive deposits, negative withdrawals, and the net amount.
- Generate an account statement header with customer details and the current date.

The ID check validates format only. It does not verify the date of birth, checksum, or authenticity of an identity number. Masking is separate from validation, and strings that are not 13 characters long are returned unchanged.

## Data Directory Setup

The setup_data_dirs script creates folders for:

- Current transactions
- Archived transactions
- Statements grouped by the current year
- Monthly reports

It also reports the number of files and subdirectories, the total file size, and the relative path and size of each file.

The base location can be supplied as a command-line argument. Without an argument, the script uses FINTRUST_DATA_DIR if set, or defaults to data/fintrust.

## Transaction Cleaning Pipeline

### Input

Both pipeline versions read data/raw_transactions.csv relative to the working directory. The expected CSV columns are:

```text
TxID,AcctID,TYPE,Amount,Date,Desc
```

### Cleaning steps

Each record is transformed into a consistent structure:

| Input field | Output field | Transformation |
|---|---|---|
| TxID | transaction_id | Removes surrounding whitespace and converts the value to an integer. |
| AcctID | account_id | Removes surrounding whitespace and converts the value to an integer. |
| TYPE | type | Removes surrounding whitespace and converts the text to lowercase. |
| Amount | amount | Removes surrounding whitespace and converts the value to a float. |
| Date | date | Converts recognised date formats to YYYY-MM-DD. |
| Desc | description | Removes surrounding whitespace and replaces empty descriptions with No description. |

Supported input date formats are YYYY-MM-DD, DD/MM/YY, and DD/MM/YYYY. Dates that do not match these formats are retained after whitespace is removed. The logging version also records a warning for an unrecognised date.

### Outputs

The pipeline writes:

- data/clean_transactions.csv: cleaned records with consistent field names.
- data/daily_summary.json: transaction counts and deposit and withdrawal totals.

The summary contains total_transactions, total_deposits, total_withdrawals, sum_deposits, and sum_withdrawals. Deposit and withdrawal totals are selected by the normalised transaction type. Amount signs are preserved, so withdrawals recorded as negative amounts produce a negative withdrawal total.

The summary covers all valid records in the input file. Despite the daily_summary filename, the code does not filter records to a specific day.

## Logging and Error Handling

The second pipeline version, clean_transaction_v2.py, builds on the original by:

- Creating data and logs directories when needed.
- Logging to both the console and logs/pipeline.log.
- Recording pipeline start, input location, and output locations.
- Checking whether the input file exists before processing.
- Reporting permission errors when reading the input.
- Including the CSV row number in conversion and missing-field errors.
- Skipping rows that raise the handled errors while continuing with the remaining records.
- Reporting how many records were processed and skipped.

This makes processing easier to trace and investigate. The current scripts perform field conversion and normalisation rather than comprehensive banking validation, and amounts are represented as floats.

## Automated Tests

### Utility tests

The test_utils suite checks currency formatting, ID masking and format checks, account types, interest calculations, fees, transaction categories, signed transaction summaries, and report header details.

### Pipeline tests

The test_pipeline suite includes:

- Date normalisation and record cleaning tests.
- A deposit and withdrawal summary test.
- An integration test checking that the logging pipeline creates its outputs.
- An integration test checking that a malformed record is skipped while valid records continue to be processed.

The integration tests create their own CSV fixtures and run the pipeline in temporary directories. They do not require a committed raw transaction file.

## Running the Project

Run the commands from the Python folder so relative data and log paths are consistent:

```text
cd week03/Python
python setup_data_dirs.py
python clean_transactions.py
python clean_transaction_v2.py
```

Before running either cleaning pipeline, place a CSV with the required columns at data/raw_transactions.csv. Both versions write to the same output paths, so running the pipeline again replaces the previous clean CSV and summary JSON.

To run the tests:

```text
python -m unittest discover -s . -p "test_*.py" -v
```

The scripts and tests currently use the Python standard library. The requirements file lists additional libraries for broader project work, but they are not imported by these scripts.

## How This Supports FinTrust

This work establishes a practical foundation for processing transaction files consistently. Reusable functions reduce repeated logic, structured outputs make records easier to analyse, and logs and tests help identify processing problems.

The files in this folder implement local Python processing. No SQL scripts or AWS deployment artifacts are included in the current Week 03 folder.
