# Week 08: Data Processing, Streaming, and Customer Workflows

Week 08 contains Python examples for catalog inspection, Athena queries, transaction streaming, Parquet processing, security-event search, and customer-support analysis.

These are standalone examples, not a deployed platform. The supplied files contain no infrastructure definitions, deployment evidence, or recorded test results. The only self-contained processing paths are the simulated Kinesis reader and local CSV-to-Parquet transformation.

## Files and Purpose

### Day 01: Athena and Glue

- [boto3_setup.py](day01/boto3_setup.py): initializes Athena and Glue clients.
- [glue_data_catalog.py](day01/glue_data_catalog.py): lists catalog databases and tables, then prints the `fintrust_curated.transactions` column schema. Database and table listings are not paginated.
- [fintrust_athena_query.py](day01/fintrust_athena_query.py): submits SQL, polls for completion, and prints account totals and transaction counts.

The Athena query selects individual transactions above R50,000 in **June 2024**, then groups them by account. Despite its source comment, it does not calculate a rolling 30-day window. Results are written to an S3 results prefix; the script retrieves only one results page and has no polling timeout.

### Day 02: Streaming and Search

- [fintrust_kineses_producer.py](day02/fintrust_kineses_producer.py): publishes five generated payment events to `transaction-stream`, using account IDs as partition keys. It also defines a batch publisher that reports failed records without retrying them.
- [record_reader.py](day02/record_reader.py): decodes base64 Kinesis payloads in a Lambda-style handler and prints transaction details. It invokes the handler locally with one simulated event.
- [opensearch.py](day02/opensearch.py): indexes a sample suspicious-login document into a monthly index, then searches for risk scores of at least 80.

No Lambda event-source mapping or streaming-to-search integration is included. The OpenSearch example requires approved endpoint and authentication configuration.

### Day 03: Parquet Processing

- [etl_script.py](day03/etl_script.py): reads four embedded CSV rows, parses timestamps, derives year/month partitions, flags amounts above 50,000, and writes Parquet locally.
- [csv_to_parquet.py](day03/csv_to_parquet.py): despite its name, uploads existing Parquet files to S3 while retaining partition paths, then lists objects under `transactions/`.
- [parquet_file_read.py](day03/parquet_file_read.py): reads a fixed S3 Parquet object, prints high-value transactions, and totals amounts by currency.

The local ETL output is:

```text
fintrust_processed/year=2024/month=06/transactions.parquet
```

The input simulates a delivery feed; no Amazon Data Firehose configuration is supplied. The upload script scans relative to the current working directory. Catalog creation and partition registration are not implemented.

### Day 04: Customer Verification and Support

- [boto3_clients.py](day04/boto3_clients.py): initializes Rekognition and Comprehend clients.
- [kyc_function.py](day04/kyc_function.py): compares two S3 images and returns match, similarity, decision, and reason fields.
- [pii_detection.py](day04/pii_detection.py): detects English-language PII and replaces detected spans with type labels, working backwards through offsets.
- [support_ticket.py](day04/support_ticket.py): defines sentiment-based routing to urgent or standard SQS queues using redacted ticket content.

**Current-code limitations:** `support_ticket.py` references `redact_pii` without defining or importing it, so calling its function as supplied raises `NameError`. Its queue URLs also require account-specific configuration. Face similarity is an example decision signal, not complete identity verification. The PII example prints its original input, which is unsuitable for sensitive production logging.

## Workflow and Boundaries

The proposed data flow is transaction ingestion, partitioned S3 storage, Glue metadata, and Athena analysis. Separate examples cover security search and customer-support routing.

The code demonstrates individual steps only. Streaming events and the embedded ETL CSV have different schemas, and no connecting transformation is supplied. Support routing likewise lacks handler wiring. Nothing here verifies AWS deployment or end-to-end execution.

## Local Setup and Safe Runs

Use Python 3, a virtual environment, and these packages:

```bash
# From the week08 directory
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install boto3 pandas pyarrow s3fs opensearch-py
```


The following examples require no AWS credentials or network access:

```bash
python day02/record_reader.py
cd day03
python etl_script.py
```

The reader prints decoded sample fields. The ETL prints data types and rows, then creates or overwrites its local Parquet output. These commands describe expected behavior, not recorded test success.

## AWS Prerequisites and Safety

Before running AWS-facing files, validate the account, permissions, region, resource ownership, data handling, and expected costs. Use facilitator-approved **Stockholm (`eu-north-1`)** for lab discussion. The scripts hardcode **`af-south-1`** as their design value; setting an AWS profile region alone does not override those client arguments.

AWS execution requires approved existing resources, appropriate IAM access, and service availability checks. Athena incurs query and storage costs; Kinesis publishing, OpenSearch indexing, S3 uploads, and SQS sends change external state. Rekognition and Comprehend submit data for service processing.

Use approved credential providers, not embedded keys. The S3 reader needs authentication configuration changes, and the OpenSearch example is not ready for authorized use as supplied. Several scripts perform AWS operations immediately when executed or imported, so review them before either action.