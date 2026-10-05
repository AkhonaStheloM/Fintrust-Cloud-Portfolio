# Week 06: SQL Analytics and AWS Inventory Audits

Week 06 combines transaction-analysis SQL with Python scripts for AWS inventory and security checks. The SQL explores suspicious transaction ratios, spending patterns, and a combined customer risk score. The Python examples use Boto3 to inspect S3 buckets, EC2 instances, and IAM users.

These files are query and script examples, not a deployed architecture. This folder contains no database schema, sample dataset, captured AWS results, or test reports. Their presence does not establish successful execution or a verified security posture.

## Files and Purposes

| File | Purpose and output |
| --- | --- |
| [day1_subqueries_ctes.txt](day1_subqueries_ctes.txt) | Uses CTEs to calculate customer suspicious transaction percentages above 5%, then compare suspicious transaction amounts between May and June 2024 for branches with increases above 20%. |
| [day2_window_functions.txt](day2_window_functions.txt) | Ranks June customer spending within spend tiers, calculates running suspicious exposure by branch, and identifies spending increases greater than three times the previous recorded month. |
| [day3_boto3.py](day3_boto3.py) | Demonstrates Boto3 clients, resources, and pagination. Prints S3 bucket metadata, EC2 instance details, a running-instance count, and object count and total size for a fixed bucket prefix. |
| [day3_audit_script.py](day3_audit_script.py) | Prints S3 bucket names, creation dates, and regions. Defines a helper that checks whether all four bucket-level public access block settings are enabled. |
| [iam_mfa_audit.py](iam_mfa_audit.py) | Finds IAM users with console login profiles but no listed MFA device. Prints the count and affected usernames with creation dates. |
| [day5_analysis_challenge.txt](day5_analysis_challenge.txt) | Combines suspicious transaction ratios with a 2024 spending-spike indicator, then returns up to 20 customers ordered by a weighted risk score. |

## Inputs, Outputs, and Workflow

### SQL analysis

Use PostgreSQL or a compatible database supporting CTEs, window functions, `DATE_TRUNC`, and PostgreSQL-style casts.

The queries expect:

- `transactions`: `transaction_id`, `customer_id`, `branch_code`, `transaction_date`, `amount`, and a suspicious-status column.
- `customers`: `customer_id`, `first_name`, and `last_name` for the spending-ranking query.

Start with Day 1 aggregation, continue with Day 2 ranking and time-series calculations, and finish with Day 5's combined scoring query. Each statement returns a result set; none creates tables or saves reports.

Check the schema before execution. Day 1 and Day 5 use `flag_suspicious`, while Day 2's running-exposure query uses `is_suspicious`. These names must match the database or be reconciled in a reviewed local copy.

### AWS inspection

The Python scripts obtain credentials through Boto3's normal credential provider chain. They print results to standard output and do not write report files. Their API operations are read-only, but execution contacts AWS and can expose account inventory in terminal output.

`day3_boto3.py` retains `af-south-1` as its code/design region for its explicit session and EC2 clients. Lab activity should use facilitator-approved Stockholm (`eu-north-1`). Setting an environment region does **not** override those explicit values. Review and adapt a local copy before running that example against a lab account. Also validate the hard-coded bucket and prefix; do not assume they exist or are authorized targets.

## Prerequisites and Local Checks

Install Python 3 and Boto3 in an isolated environment. From the `week06` directory:

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install boto3
python -m py_compile day3_boto3.py day3_audit_script.py iam_mfa_audit.py
```

Compilation checks syntax without executing AWS calls, but creates local bytecode cache files. It does not verify credentials, permissions, or runtime behavior.

For SQL, connect to an authorized local PostgreSQL database containing suitable non-sensitive data:

```bash
psql -d fintrust_local -v ON_ERROR_STOP=1 -f day1_subqueries_ctes.txt
psql -d fintrust_local -v ON_ERROR_STOP=1 -f day2_window_functions.txt
psql -d fintrust_local -v ON_ERROR_STOP=1 -f day5_analysis_challenge.txt
```

Use your actual local database name.

Before AWS execution, confirm the approved account, profile, Stockholm region, API permissions, and any applicable request costs. Required access includes S3 bucket/location/object listing, EC2 instance descriptions, and IAM user/login-profile/MFA inspection. After approval, the default-region scripts can be run with an authorized profile:

```bash
$env:AWS_PROFILE = "approved-lab"
$env:AWS_DEFAULT_REGION = "eu-north-1"
python day3_audit_script.py
python iam_mfa_audit.py
```

## Current-Code Limitations

- Day 1's “Top 10” comment is inaccurate: the query has no `LIMIT`. Its branch comparison excludes branches missing either month and can divide by zero when May totals are zero.
- `LAG` compares recorded months, not necessarily consecutive calendar months. Day 5 uses an inclusive three-times threshold; Day 2 uses a strict threshold.
- The S3 public-access helper is defined but never called. Bucket-level settings alone are not a complete public-access assessment.
- The IAM check covers console-enabled IAM users only. It does not assess root-user or federated MFA, nor prove MFA enforcement.
- AWS access failures are largely unhandled, and the initial EC2 inventory call is not paginated.