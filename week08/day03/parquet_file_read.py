import pandas as pd

# Read Parquet directly from S3 using s3fs
df = pd.read_parquet(
    's3://fintrust-processed/transactions/year=2024/month=06/transactions.parquet',
    engine='pyarrow',
    storage_options={'key': 'YOUR_ACCESS_KEY', 'secret': 'YOUR_SECRET_KEY'}
    # Or leave storage_options empty if using IAM roles (e.g. on EC2 or Cloud9)
)

# Query 1: filter for high-value transactions
high_value = df[df['is_high_value'] == True]
print(f'High-value transactions: {len(high_value)}')
print(high_value[['account_id', 'amount', 'currency']])

# Query 2: total amount by currency
by_currency = df.groupby('currency')['amount'].sum().reset_index()
by_currency.columns = ['currency', 'total_amount']
print(by_currency)