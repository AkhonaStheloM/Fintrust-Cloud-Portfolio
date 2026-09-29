# Week 1 — Cloud and SQL Foundations

## Status

Week 1 SQL files are uploaded to GitHub and the five critical syntax/filter fixes identified in review have been applied to the branches and WHERE challenge files. The official route is the Day 2 `fintrust` schema; `day4_where_filtering.sql` now also uses `fintrust`. The alternative Day 3 `fintrust_db` schema remains a separate learning exercise. No live SQL execution has been performed because no database environment is connected.

## What This Week Covers

### Cloud / AWS foundations

- AWS Regions and Availability Zones
- VPC fundamentals, including public and private subnets
- Internet Gateway (IGW) and NAT Gateway
- Stateful Security Groups versus stateless Network ACLs
- FinTrust three-tier VPC design in `af-south-1`

### SQL foundations

- Database, table, column, row, and data-type concepts
- The FinTrust `customers`, `accounts`, and `transactions` tables
- `CREATE TABLE`, `INSERT INTO`, and `SELECT`
- Filtering with `=`, `!=`, `>`, `<`, `LIKE`, `IN`, `BETWEEN`, `IS NULL`, and `IS NOT NULL`
- Primary keys, foreign keys, unique constraints, and basic relationships

## Current Files

| File | Purpose |
|---|---|
| `day2_basic_select.sql` | Basic `SELECT`, ordering, filtering, `DISTINCT`, calculations, and `COUNT` exercises |
| `day2_create_fintrust_database_table.sql` | Creates the `fintrust` database and the three main tables with the larger 10-row dataset structure |
| `day2_data_verification.sql` | Checks expected row counts for customers, accounts, and transactions |
| `day2_explore.sql` | Exploratory queries for customers, active accounts, provinces, and balances |
| `day2_insert_data.sql` | Inserts the 10-customer, 10-account, and 10-transaction dataset |
| `day3_branches_challenge.sql` | Adds branches and links accounts to branches |
| `day3_fintrust_schema.sql` | Alternative five-row schema and sample dataset using `fintrust_db` |
| `day4_where_challenge.sql` | `WHERE` clause challenge queries |
| `day4_where_filtering.sql` | Extended `WHERE` filtering practice using `fintrust` |

## Critical Review Findings and Current Status

These are correctness or execution blockers, not cosmetic suggestions.

1. **Database-name decision recorded.** The recommended official Week 1 route is the Day 2 `fintrust` schema. `day4_where_filtering.sql` has been updated to use `USE fintrust;`. The separate `day3_fintrust_schema.sql` exercise still uses `fintrust_db` and should not be run as part of the official `fintrust` sequence without further reconciliation.

2. **There are two different schema/data designs.** `day2_create_fintrust_database_table.sql` plus `day2_insert_data.sql` define the 10-row dataset and include columns such as `id_number`, `phone`, `status`, `opened_date`, `description`, and `reference_no`. `day3_fintrust_schema.sql` defines a different five-row dataset with fewer columns. These scripts should not be treated as one uninterrupted setup sequence.

3. **Resolved — `day3_branches_challenge.sql`.** The branch `INSERT` column list now uses `branch_name, province`, and the second account update now uses `account_id`. The file was uploaded to `main` after review. Its rerun assumptions remain documented below.

4. **Resolved — `day4_where_challenge.sql`.** The province query now uses `NOT IN`, the balance range is `BETWEEN 1000 AND 2000`, and the merchant-category filter uses `IN ('Groceries', 'Food')`. The corrected file was uploaded to `main` after review.

5. **The verification counts do not match every schema file.** `day2_data_verification.sql` expects 10 customers, 10 accounts, and 10 transactions, which matches `day2_insert_data.sql`. It does not match the five-row dataset in `day3_fintrust_schema.sql`.

6. **The scripts have different run assumptions.** Some files begin with `USE`, while `day2_data_verification.sql` assumes a database and tables have already been selected. The files should be run in a documented order after choosing the intended schema.

7. **Several setup scripts are not safely repeatable.** Re-running the insert scripts can create duplicate-key errors, and re-running the branch challenge can fail when the branch column or foreign-key constraint already exists. This is acceptable for a learning exercise only if the README explains the intended fresh-database run order.

## Recommended Run Decision

The recommended route is the Day 2 `fintrust` setup as the main Week 1 dataset. Keep the separate Day 3 `fintrust_db` practice schema clearly separate, and do not mix the two without reconciling their database names, columns, row counts, and transaction types.

A clean submission should then:

1. Use one consistent database name.
2. Use one agreed schema and seed-data source.
3. Correct the critical syntax and filter errors in the branches and WHERE challenge files.
4. Document the run order and expected results.
5. Keep the learner's own reflection and AWS notes in the portfolio.

## Praesignis Week 1 Requirements

Based on the Praesignis Cloud to Solutions Accelerator Week 1 guidance and Portfolio Check-In #1 instructions:

### Expected portfolio structure

```text
fintrust-cloud-portfolio/
├── README.md
└── week01/
    ├── README.md
    ├── sql/
    │   ├── day3_fintrust_schema.sql
    │   ├── day4_where_queries.sql
    │   └── day4_where_challenges.sql   # if completed
    └── notes/
        ├── day1_reflection.md
        └── week1_aws_notes.md
```

The current repository has the SQL files directly under `week01/`, so the `sql/` and `notes/` organisation still needs to be completed if you want to match the recommended structure exactly.

### Minimum Check-In #1 requirements

- A public GitHub repository named `fintrust-cloud-portfolio` with a root `README.md`.
- At least one committed SQL file containing all three FinTrust `CREATE TABLE` statements: `customers`, `accounts`, and `transactions`.
- A written reflection of at least three sentences in `week01/notes/` or `week01/README.md`.
- The repository URL submitted in the Week 1 Day 5 Portfolio Check-In #1 LMS assignment.
- The repository must remain public so the facilitator can review it.

### Stretch / presentation items

- Both the schema SQL and WHERE-query SQL are committed.
- A structured `week01/README.md` explains what was learned and lists the files.
- AWS notes cover Regions and Availability Zones, VPC public/private subnets, IGW, NAT Gateway, Security Groups versus NACLs, and the FinTrust three-tier design in `af-south-1`.

## Learner-Owned Reflection

Add your own reflection here or in `week01/notes/`. Praesignis asks for at least three sentences. Explain what you learned, what was most challenging, what became clearer, and what you still want to revisit. This section is intentionally left for the learner's own words.

## Source

Praesignis Cloud to Solutions Accelerator course: <https://edusignis.praesignis.com/course/view.php?id=119>
