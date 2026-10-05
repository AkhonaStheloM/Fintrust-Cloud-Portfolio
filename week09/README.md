# Week 09: Cost Management, Governance and Migration Utilities

Week 09 contains Python examples for AWS pricing, cost reporting, budgets, tag compliance, Service Catalog inventory, migration planning and operational status checks.

The work consists of standalone scripts and client setup snippets. There is no deployment configuration, automated test suite or captured AWS execution evidence in the supplied files. FinTrust amounts, instance types and data volumes are scenario inputs, not verified account measurements.

## File Guide

### Day 01: Pricing and Savings Estimates

- [`boto3_pricing.py`](day01/boto3_pricing.py) creates a Pricing API client in `us-east-1`. It does not request prices or print results.
- [`ec2_pricing.py`](day01/ec2_pricing.py) queries Linux, shared-tenancy EC2 On-Demand prices for `m5.xlarge`, `r5.2xlarge` and `c5.large`. It prints hourly prices and monthly estimates using 730 hours. The workload region defaults to `af-south-1`.
- [`fintrust_compute_savings_plan.py`](day01/fintrust_compute_savings_plan.py) calculates an illustrative three-year commitment using $32.47/hour and an assumed 66% discount. It prints commitment, estimated comparative costs and savings. It neither retrieves a Savings Plans quote nor purchases a plan.

The savings calculation assumes the stated discount and full utilization throughout the term. Actual pricing, coverage and realized savings require separate validation.

### Day 02: Spend Visibility and Budgets

- [`query_monthly.py`](day02/query_monthly.py) requests June 2024 monthly `UnblendedCost` from Cost Explorer, grouped by service. It excludes amounts at or below $0.01, sorts the remaining results and prints the ten largest.
- [`budget_creation.py`](day02/budget_creation.py) discovers the caller’s account through STS, creates a $15,000 monthly cost budget with an actual-spend alert above 80%, then prints budget utilization from a listing response.

Budget creation runs at module level, including when imported. It is an account-modifying operation, not a dry run. The configured email is a scenario recipient and must be reviewed before any authorized execution.

### Day 03: Governance Inventory

- [`api_tagging.py`](day03/api_tagging.py) initializes a regional Resource Groups Tagging API client.
- [`portfolio_products_list.py`](day03/portfolio_products_list.py) combines accepted shared and owned Service Catalog portfolios, deduplicates them by ID and prints their products. Product provisioning is commented out and is not implemented as an active workflow.
- [`tag_compliance_report.py`](day03/tag_compliance_report.py) paginates tagging results and checks for `CostCentre`, `Team` and `Environment` keys. It prints violation counts and up to three examples per AWS service.

The tag report checks key presence, not acceptable values. Its scope is resources returned by the tagging API, not a complete inventory of every untagged resource. Service Catalog listing does not implement pagination.

### Day 04: Migration and Operational Checks

- [`device_capacity_reference.py`](day04/device_capacity_reference.py) uses a static device-capacity table to estimate quantities. Its 3,000 TB archive example produces a device count, total capacity and unused capacity.
- [`dms_client_setup.py`](day04/dms_client_setup.py) attempts to initialize a migration-service client.
- [`polling_monitor_implementation.py`](day04/polling_monitor_implementation.py) defines functions for reading replication-task progress and polling status. The example invocation is commented out.
- [`status_checker.py`](day04/status_checker.py) lists FIS experiments and retrieves details for up to ten, printing state, template, start time and a stop condition. It does not start experiments.

**Current-code limitation:** both DMS files use `database-migration-service` as the Boto3 service name. Boto3 uses `dms`, so client initialization is expected to fail before monitoring can run.

The device table is a historical planning reference, not a current availability or ordering guide. Validate current transfer offerings, eligibility and regional availability independently. No transfer, database migration, archive upload or resilience experiment is deployed here.

## Workflow and Inputs/Outputs

The examples progress from estimating compute costs to inspecting spend, reviewing governance metadata and checking operational status. They are not connected into an automated pipeline.

Inputs are hardcoded scenario values, account data returned by AWS and, for the monitor function, a task ARN supplied by an operator. Outputs are console text or returned Python dictionaries. No report files are written.

`af-south-1` remains the code’s design region, not an authorized lab region. Use facilitator-approved Stockholm (`eu-north-1`) for lab discussion. The EC2 pricing lookup does not currently include Stockholm in its region-name mapping. Billing clients explicitly use `us-east-1`, separately from workload-region choices.

## Prerequisites and Safe Local Use

From the `week09` directory, use Python 3 and an isolated environment:

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install boto3
python -m compileall day01 day02 day03 day04
python day01/fintrust_compute_savings_plan.py
python day04/device_capacity_reference.py
```


Before AWS-connected execution, validate credentials, account identity, facilitator-approved region, least-privilege permissions and possible API charges. Cost Explorer also requires accessible billing data; June 2024 may be outside available history. Review hardcoded inputs first.

Do not run or import the budget script without explicit authorization, recipient confirmation and budget-cost review. Read-only reports still expose account information. None of the supplied files demonstrates successful runtime execution.