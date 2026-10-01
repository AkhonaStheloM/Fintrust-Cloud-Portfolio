import boto3

# Region-scoped: query tagging data for resources in af-south-1
tagging = boto3.client('resourcegroupstaggingapi', region_name='af-south-1')