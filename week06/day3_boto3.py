import boto3

# Create a session (uses default profile from ~/.aws/credentials)
session = boto3.Session(
    region_name='af-south-1'  # Cape Town region for FinTrust
)

# Create a client (low-level)
s3_client = session.client('s3')

# Create a resource (high-level, where available)
s3_resource = session.resource('s3')

# Quick test: list S3 buckets
response = s3_client.list_buckets()
for bucket in response['Buckets']:
    print(bucket['Name'], bucket['CreationDate'])
    

ec2 = boto3.client('ec2', region_name='af-south-1')

# describe_instances returns a paginated result
response = ec2.describe_instances()

for reservation in response['Reservations']:
    for instance in reservation['Instances']:
        instance_id = instance['InstanceId']
        state = instance['State']['Name']
        instance_type = instance['InstanceType']

        # Get the Name tag (if it exists)
        name = '(no name)'
        for tag in instance.get('Tags', []):
            if tag['Key'] == 'Name':
                name = tag['Value']

        print(f"{instance_id:20} {state:10} {instance_type:15} {name}")
        
ec2 = boto3.client('ec2', region_name='af-south-1')

# Create a paginator for describe_instances
paginator = ec2.get_paginator('describe_instances')

# Filter: only running instances
page_iterator = paginator.paginate(
    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}]
)

instances = []
for page in page_iterator:
    for reservation in page['Reservations']:
        instances.extend(reservation['Instances'])

print(f"{len(instances)} running instances found")

s3 = boto3.client('s3')

# Paginate through objects in the FinTrust transactions bucket
paginator = s3.get_paginator('list_objects_v2')
pages = paginator.paginate(
    Bucket='fintrust-transactions-prod',
    Prefix='2024/06/'  # June 2024 objects only
)

total_size = 0
object_count = 0
for page in pages:
    for obj in page.get('Contents', []):
        total_size += obj['Size']
        object_count += 1

print(f"{object_count} objects, {total_size / 1024 / 1024:.1f} MB total")
