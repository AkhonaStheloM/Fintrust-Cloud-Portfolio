import boto3

# Client: low-level, maps directly to AWS API calls
# Use for SQS, SNS, EventBridge — services without a Resource API
sqs = boto3.client('sqs', region_name='af-south-1')
sns = boto3.client('sns', region_name='af-south-1')

# Resource: higher-level OO interface
# Available for S3, DynamoDB, SQS, EC2 — not all services
s3 = boto3.resource('s3')
bucket = s3.Bucket('fintrust-documents')
for obj in bucket.objects.all():
    print(obj.key)

# Inside Lambda: credentials come from the execution role
# Do NOT pass Access Key / Secret Key — use IAM roles
# boto3 automatically uses LAMBDA_TASK_ROOT + AWS_* env vars