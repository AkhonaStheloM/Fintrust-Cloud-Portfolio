import boto3

glue = boto3.client('glue', region_name='af-south-1')

# 1. List all databases in the catalog
db_response = glue.get_databases()
for db in db_response['DatabaseList']:
    print(f"Database: {db['Name']}")

# 2. List tables in the fintrust_curated database
tbl_response = glue.get_tables(DatabaseName='fintrust_curated')
for tbl in tbl_response['TableList']:
    print(f"  Table: {tbl['Name']} | Location: {tbl['StorageDescriptor']['Location']}")

# 3. Get the full schema of the transactions table
tbl_detail = glue.get_table(
    DatabaseName='fintrust_curated',
    Name='transactions'
)
columns = tbl_detail['Table']['StorageDescriptor']['Columns']
print('\nTransactions table schema:')
for col in columns:
    print(f"  {col['Name']:25s} {col['Type']}")