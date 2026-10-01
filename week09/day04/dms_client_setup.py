import boto3

# Note: service name is 'database-migration-service', not 'dms'
dms = boto3.client('database-migration-service', region_name='af-south-1')