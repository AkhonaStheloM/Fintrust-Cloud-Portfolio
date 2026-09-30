# Week 4 Reflection

## Q1: Why split one PostgreSQL database into seven services?

A single PostgreSQL database could technically store all FinTrust data, but it would not be optimized for every workload. Each AWS service was selected for a specific capability: RDS PostgreSQL for ACID-compliant banking transactions, DynamoDB Global Tables for active-active session management, QLDB for cryptographically verifiable audit records, DocumentDB for flexible JSON documents, Redis for sub-millisecond caching, and Redshift for large-scale analytics. This architecture improves performance and scalability because each service handles the workload it was designed for. The trade-off is increased operational complexity, including more monitoring dashboards, IAM permissions, backup strategies, and service costs to manage.

## Q2: How would the ETL pipeline behave differently on SQLite versus RDS Multi-AZ?

SQLite is a file-based database and can experience write contention when multiple processes attempt to write simultaneously because the database file becomes locked. This makes it suitable for learning and small local applications but less suitable for production-scale systems. RDS Multi-AZ provides a synchronous standby in another Availability Zone and automatic failover within approximately 60 to 120 seconds if the primary instance fails. However, Multi-AZ solves availability problems, not performance problems. Read scaling still requires Read Replicas, and high-volume concurrent workloads may still require connection pooling and proper database design.

## Q3: What is the benefit of converting the ETL pipeline into a Python package?

Splitting the pipeline into separate modules improves maintainability, testing, and reusability. For example, the \`validate_row()\` function in \`loader.py\` can be tested independently without creating a database connection. If FinTrust later migrates from SQLite to PostgreSQL, only the code in \`database.py\` needs to change while the validation logic remains untouched. This modular structure also supports CI/CD pipelines because automated tests can import individual modules and test specific functionality without executing the entire application.

## Q4: How does Week 4 connect to Week 5 networking concepts?

The database architecture designed in Week 4 relies heavily on networking concepts that will be covered in Week 5. RDS PostgreSQL should be deployed in a private subnet so it is not directly accessible from the public internet and can only be reached through private VPC routing. DynamoDB can be accessed through a Gateway Endpoint, allowing traffic between AWS resources and DynamoDB to remain on the AWS network instead of traversing the public internet. These networking controls improve security, reduce exposure, and support financial compliance requirements. Understanding VPC design is therefore essential for securely operating the database services selected during Week 4.
