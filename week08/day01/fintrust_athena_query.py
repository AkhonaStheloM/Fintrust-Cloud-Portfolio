import boto3, time

athena = boto3.client('athena', region_name='af-south-1')

def run_athena_query(sql, database, output_bucket):
    response = athena.start_query_execution(
        QueryString=sql,
        QueryExecutionContext={'Database': database},
        ResultConfiguration={'OutputLocation': f's3://{output_bucket}/athena-results/'}
    )
    query_id = response['QueryExecutionId']

    while True:
        status = athena.get_query_execution(QueryExecutionId=query_id)
        state = status['QueryExecution']['Status']['State']
        if state in ('SUCCEEDED', 'FAILED', 'CANCELLED'):
            break
        time.sleep(1)

    if state != 'SUCCEEDED':
        raise RuntimeError(f'Query failed: {state}')

    results = athena.get_query_results(QueryExecutionId=query_id)
    return results['ResultSet']['Rows']

# FinTrust compliance query: transactions over R50,000 in last 30 days
sql = """
SELECT account_id, SUM(amount) as total, COUNT(*) as tx_count
FROM fintrust_curated.transactions
WHERE year = '2024' AND month = '06'
  AND amount > 50000
GROUP BY account_id
ORDER BY total DESC
LIMIT 100
"""

rows = run_athena_query(sql, 'fintrust_curated', 'fintrust-athena-results')
for row in rows[1:]:  # skip header row
    vals = [c.get('VarCharValue', '') for c in row['Data']]
    print(f'Account: {vals[0]}, Total: {vals[1]}, Transactions: {vals[2]}')