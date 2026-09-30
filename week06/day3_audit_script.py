import boto3

s3 = boto3.client('s3')
response = s3.list_buckets()

for bucket in response['Buckets']:
    name = bucket['Name']
    created = bucket['CreationDate'].strftime('%Y-%m-%d')

    # get_bucket_location for each bucket (separate API call)
    loc = s3.get_bucket_location(Bucket=name)
    region = loc['LocationConstraint'] or 'us-east-1'

    print(f"{name:45} {created}  {region}")
    
def is_public_access_blocked(s3_client, bucket_name):
    try:
        r = s3_client.get_public_access_block(Bucket=bucket_name)
        config = r['PublicAccessBlockConfiguration']
        return all([
            config.get('BlockPublicAcls', False),
            config.get('IgnorePublicAcls', False),
            config.get('BlockPublicPolicy', False),
            config.get('RestrictPublicBuckets', False),
        ])
    except s3_client.exceptions.NoSuchPublicAccessBlockConfiguration:
        return False  # No block = not safe
