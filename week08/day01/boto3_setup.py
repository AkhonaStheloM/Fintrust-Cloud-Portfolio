import boto3

# Athena client — specify the region where your data lake lives
athena = boto3.client('athena', region_name='af-south-1')

# Glue client — same region as the Data Catalog
glue = boto3.client('glue', region_name='af-south-1')