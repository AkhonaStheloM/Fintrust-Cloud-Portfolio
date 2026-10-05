# Week 07: Transaction APIs and Event-Driven Processing

Week 07 contains local transaction API prototypes, Lambda event-handler examples, and Boto3 examples for object listing and fraud alerts. The work progresses from HTTP request handling to AWS event parsing and rule-based transaction scoring.

These files are source examples, not evidence of an AWS deployment or successful test run. No infrastructure definitions, automated tests, dependency manifest, or deployment instructions are included in the supplied week folder.

## File Guide

| File | Purpose |
| --- | --- |
| [day01/app.py](day01/app.py) | Flask API with health checks, transaction creation, and optional account filtering. |
| [day01/main.py](day01/main.py) | FastAPI equivalent with request validation and typed transaction responses. |
| [day01/extension_exercise.py](day01/extension_exercise.py) | Extended FastAPI application with transaction lookup, status updates, and an `X-Request-ID` response header. |
| [day02/api_gateway.py](day02/api_gateway.py) | Parses an API Gateway REST API proxy event and returns its decoded body. |
| [day02/lambda_function.py](day02/lambda_function.py) | Logs event and Lambda context information, then returns a proxy-style response. |
| [day02/s3_event.py](day02/s3_event.py) | Extracts bucket name, object key, and size from S3 event records. |
| [day02/sqs_event.py](day02/sqs_event.py) | Illustrates parsing and processing an SQS message batch. |
| [day04/client_resource.py](day04/client_resource.py) | Demonstrates Boto3 clients and resources, including listing objects in a named S3 bucket. |
| [day04/fraud_scorer.py](day04/fraud_scorer.py) | Scores transactions from SQS-style records and publishes qualifying alerts to SNS. |

## Workflow and Inputs/Outputs

### Local transaction APIs

All three Day 01 applications expose:

- `GET /health`: returns `{"status": "ok"}`.
- `POST /transactions`: accepts transaction JSON and returns a generated UUID, `pending` status, and UTC timestamp with HTTP 201.
- `GET /transactions`: returns stored transactions, optionally filtered by `account_id`.

The Flask implementation checks for `account_id`, `amount`, and `currency`, but does not validate their values. The FastAPI implementations require a nonempty account identifier, a positive amount no greater than 1,000,000, and a three-uppercase-letter currency string. This checks formatting, not membership in an ISO currency registry. An optional description is also accepted.

The extension adds `GET /transactions/{transaction_id}` and `PATCH /transactions/{transaction_id}/status`, accepting only `approved` or `rejected`. Unknown transaction IDs return HTTP 404.

Each application uses its own process-local list. Data disappears when the process restarts and is not shared across applications or workers. There is no authentication or durable database integration.

### Event processing and proposed architecture

Day 02 separates trigger payload examples:

- API Gateway input uses `httpMethod`, `path`, and a JSON-string `body`. The handler echoes the decoded body; reading an authorization header does not authenticate callers.
- The logging handler requires a Lambda-like context and returns HTTP 200 with a JSON `message`.
- S3 and SQS examples consume an event containing `Records`.

A proposed event-driven arrangement could connect transaction ingestion to SQS, then invoke the fraud scorer and publish alerts through SNS. The repository does not implement that connection or provision those services.

The scorer uses amount bands, non-`ZAR` currency, and selected description keywords. It logs scores and publishes alert JSON when the score reaches `HIGH_RISK_THRESHOLD`, defaulting to `75.0`. It requires `ALERT_TOPIC_ARN`. Current rules produce at most 75 points.

## Local Setup and Run

Use Python 3.10 or 3.11, a virtual environment, and `curl` or an HTTP client. From the `week07` directory:

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install flask "fastapi>=0.95,<0.100" "pydantic>=1.10,<2" uvicorn
python -m uvicorn day01.main:app --host 127.0.0.1 --port 8000
```

The version constraints accommodate the source’s Pydantic v1 `validator` and `Field(regex=...)` usage. Open `http://127.0.0.1:8000/docs`, or submit:

```bash
curl -X POST http://127.0.0.1:8000/transactions \
  -H "Content-Type: application/json" \
  -d '{"account_id":"demo-account","amount":125.50,"currency":"ZAR"}'

curl "http://127.0.0.1:8000/transactions?account_id=demo-account"
```

For the extension, replace `day01.main:app` with `day01.extension_exercise:app`. Run Flask separately with `python day01/app.py`; it uses port 5000 and enables development debugging.

## Current Limitations and AWS Safety

The S3 example references an undefined `logger`. The SQS example references both an undefined `logger` and `process_transaction`. They are incomplete runtime examples. The fraud scorer also assumes `description` is a string, so an explicit JSON `null` can cause failure. The logging handler records entire events; avoid sensitive transaction data.

Before executing Day 04 files, validate the AWS account, permissions, region, resource ownership, and costs. Importing `client_resource.py` initiates S3 listing; invoking the scorer can publish real SNS notifications. Use temporary credentials or IAM roles, never embedded keys.

The code’s explicit `af-south-1` client region is a design value, not lab authorization. Lab discussion should use facilitator-approved Stockholm (`eu-north-1`). Other Boto3 calls use configured defaults, so review region selection before any authorized AWS execution.