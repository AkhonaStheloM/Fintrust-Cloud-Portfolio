import boto3, json, uuid, datetime

kinesis = boto3.client('kinesis', region_name='af-south-1')
STREAM_NAME = 'transaction-stream'

def publish_transaction(account_id, amount, currency, tx_type):
    event = {
        'transaction_id': str(uuid.uuid4()),
        'account_id': account_id,
        'amount': amount,
        'currency': currency,
        'type': tx_type,
        'timestamp': datetime.datetime.utcnow().isoformat()
    }
    response = kinesis.put_record(
        StreamName=STREAM_NAME,
        Data=json.dumps(event).encode('utf-8'),
        PartitionKey=account_id  # same account always hits same shard
    )
    return response['SequenceNumber'], response['ShardId']

# Test with 5 transactions across 3 distinct accounts
for i in range(5):
    seq, shard = publish_transaction(
        account_id=f'ACC-{i % 3:04d}',  # only 3 distinct accounts
        amount=round(1000 * (i + 1), 2),
        currency='ZAR',
        tx_type='PAYMENT'
    )
    print(f'Published to {shard}, sequence: {seq[:20]}...')
    
def publish_batch(transactions):
    records = [
        {
            'Data': json.dumps(txn).encode('utf-8'),
            'PartitionKey': txn['account_id']
        }
        for txn in transactions
    ]
    response = kinesis.put_records(StreamName=STREAM_NAME, Records=records)
    failed = response['FailedRecordCount']
    if failed > 0:
        print(f'Warning: {failed} records failed')
    return len(records) - failed
