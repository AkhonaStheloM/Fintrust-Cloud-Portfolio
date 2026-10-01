import boto3, pathlib

s3 = boto3.client('s3', region_name='af-south-1')
BUCKET = 'fintrust-processed'

def upload_parquet_partition(local_path, s3_key):
    s3.upload_file(local_path, BUCKET, s3_key)
    print(f'Uploaded s3://{BUCKET}/{s3_key}')

# Upload all .parquet files maintaining the partition structure
for f in pathlib.Path('.').glob('fintrust_processed/**/*.parquet'):
    # Strip the local prefix and use the partition path as the S3 key
    s3_key = 'transactions/' + str(f).replace('fintrust_processed/', '').replace('\\', '/')
    upload_parquet_partition(str(f), s3_key)
    
    # List objects in the transactions prefix to confirm structure
paginator = s3.get_paginator('list_objects_v2')
for page in paginator.paginate(Bucket=BUCKET, Prefix='transactions/'):
    for obj in page.get('Contents', []):
        size_kb = obj['Size'] // 1024
        print(f'  {obj["Key"]} ({size_kb} KB)')
