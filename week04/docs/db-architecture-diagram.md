# FinTrust 7-Layer Database Architecture

## Architecture Diagram

┌─────────────────────────────────────────────────────────────┐
│ L1: RDS PostgreSQL Multi-AZ (af-south-1)                   │
│ Role: Core transaction engine                              │
│ Why: ACID compliance, financial integrity, failover        │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ L2: Aurora PostgreSQL Read Replica (af-south-1)            │
│ Role: Reporting and analytics                              │
│ Why: Offloads read traffic from primary database           │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ L3: DynamoDB Global Tables                                 │
│ Regions: af-south-1 + eu-west-1                            │
│ Role: Session tokens and login state                       │
│ Why: Active-active multi-region replication                │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ L4: Amazon QLDB (af-south-1)                               │
│ Role: Regulatory audit ledger                              │
│ Why: Immutable records and cryptographic verification      │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ L5: Amazon DocumentDB (af-south-1)                         │
│ Role: Trade confirmation documents                         │
│ Why: Flexible JSON document storage                        │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ L6: ElastiCache Redis (af-south-1)                         │
│ Role: FX rates and leaderboard cache                       │
│ Why: Sub-millisecond in-memory performance                 │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ L7: Amazon Redshift (af-south-1)                           │
│ Role: Historical analytics and reporting                   │
│ Why: OLAP, columnar storage, MPP architecture              │
└─────────────────────────────────────────────────────────────┘

-------------------------------------------------------------

Migration Layer

AWS DMS with CDC
Region: af-south-1

Role:
- Migrates transaction data into AWS

Why:
- Zero-downtime migration
- Captures ongoing changes during migration
- No SCT required for PostgreSQL-to-PostgreSQL migration

-------------------------------------------------------------

## Summary Table

| Layer | Service | Region | Why |
|--------|----------|---------|------|
| L1 | RDS PostgreSQL Multi-AZ | af-south-1 | ACID transactions and automatic failover |
| L2 | Aurora PostgreSQL Read Replica | af-south-1 | Read scaling and reporting |
| L3 | DynamoDB Global Tables | af-south-1, eu-west-1 | Active-active multi-region access |
| L4 | Amazon QLDB | af-south-1 | Immutable audit trail |
| L5 | Amazon DocumentDB | af-south-1 | Flexible JSON document storage |
| L6 | ElastiCache Redis | af-south-1 | High-speed caching |
| L7 | Amazon Redshift | af-south-1 | Data warehouse and analytics |
| Migration | AWS DMS + CDC | af-south-1 | Zero-downtime migration |
