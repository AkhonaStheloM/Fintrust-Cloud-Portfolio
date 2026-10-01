import boto3

# Pricing API is ALWAYS us-east-1 regardless of where your workload runs
pricing = boto3.client('pricing', region_name='us-east-1')