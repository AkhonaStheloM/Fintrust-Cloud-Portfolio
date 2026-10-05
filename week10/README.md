# Week 10: Migration Portfolio and Transfer Helpers

Week 10 contains migration inventory logic, database reporting views, and draft helpers for AWS DMS and DataSync. The files support grouping EC2 assets into migration strategies and waves, reporting migration progress, inspecting replication lag, and proposing scheduled transfer bandwidth changes.

This folder is source material, not a complete migration application or deployment. No infrastructure definitions, deployment evidence, tests, or execution results are included in the supplied files.

## File Guide

| File | Purpose |
| --- | --- |
| [`_init_.py`](_init_.py) | Attempts to expose session, EC2 classification, and DMS helper functions through package-level imports. |
| [`clssifier.py`](clssifier.py) | Reads EC2 instance tags and groups assets by migration strategy and wave. The filename is spelled this way in the repository. |
| [`dms_helpers.py`](dms_helpers.py) | Contains intended DMS task inspection, start/stop, status polling, and CloudWatch CDC latency helpers. |
| [`migration_views.sql`](migration_views.sql) | Defines portfolio and wave-progress views, then queries low-completion waves and overall completion. |
| [`sync_helpers.py`](sync_helpers.py) | Contains a DataSync bandwidth-update function and a proposed Lambda handler for scheduled mode changes. |

## Workflow and Inputs/Outputs

### EC2 migration inventory

`classify_instances()` paginates through EC2 instances and reads `migration:strategy` and `migration:wave` tags by default. Supported strategy values are `rehost`, `replatform`, `refactor`, `retire`, `retain`, and `repurchase`.

It returns a strategy-to-instance mapping plus a separate list for missing or unsupported strategy values. Each entry contains an instance ID, wave, and strategy. `get_migration_wave()` filters recognized strategies by the string representation of a supplied wave number. Instances with invalid strategies are therefore excluded from its result.

### SQL progress reporting

The SQL expects existing `asset_register` and `migration_plan` tables with the referenced columns.

- `v_migration_portfolio` joins asset and migration records, excluding assets whose `decommission_flag` is not zero.
- `v_wave_progress` counts all migration-plan rows by wave and calculates completion from status `C`. It also counts `I` as in progress and `F` as failed.
- Final queries identify waves below 50% completion and calculate overall portfolio completion.

These views use different populations: the wave summary does not apply the portfolio view’s decommission filter. The script creates or replaces database objects, so it is not a read-only report.

### DMS and DataSync helpers

The intended DMS workflow accepts a task ARN, retrieves status and statistics, and polls for a requested state. Starting or stopping a task changes AWS replication activity.

The latency logic requests recent maximum `CDCLatencySource` and `CDCLatencyTarget` metrics. Its proposed readiness flag checks only whether source latency is below 30 seconds. That is not sufficient evidence for a safe cutover, data consistency, or guaranteed zero downtime.

The DataSync handler reads `DATASYNC_TASK_ARN` and an event `mode`. It proposes 500 Mbps for `daytime` and 9000 Mbps for `overnight`, defaulting unknown modes to 500 Mbps. Comments describe SAST time windows, but no scheduler configuration is supplied. These settings represent design intent, not an AWS deployment.

## Current Code Limitations

- `_init_.py` is not Python’s conventional `__init__.py`. Its imports reference `utils`, `ec2`, and `rds` package paths absent from this folder.
- `clssifier.py` and `dms_helpers.py` depend on a parent-relative session helper that is not supplied here.
- `dms_helpers.py` has malformed function indentation and cannot currently be parsed as valid Python.
- `sync_helpers.py` calls `get_client` without defining or importing it. Its comment treating zero as unlimited should not be used as API guidance; validate current DataSync option semantics and task-mode support before any update.

## Prerequisites and Local Checks

Local source inspection requires Python 3. AWS integration would additionally require Boto3, working session helpers, appropriate IAM permissions, existing resources, and approved credentials supplied outside source code. SQL execution requires a compatible database dialect, the expected tables, and permission to manage views.

From the repository root, perform a local syntax check without contacting AWS:

```bash
cd week10
python -m compileall .
```

This checks parsing only, not imports or functionality.

Before any AWS operation, validate the account, resource identifiers, permissions, region, and cost implications. Use facilitator-approved Stockholm (`eu-north-1`) for lab discussion and authorized lab activity. Do not infer an authorized region from missing session configuration. Review database changes in an isolated environment before applying the SQL.