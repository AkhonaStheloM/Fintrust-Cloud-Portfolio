import json

def lambda_handler(event, context):
    # SQS delivers a batch of records
    for record in event['Records']:
        body = json.loads(record['body'])
        queue_arn = record['eventSourceARN']
        message_id = record['messageId']

        logger.info('Processing message %s from %s', message_id, queue_arn)
        process_transaction(body)
    # Return nothing: Lambda reports success (no return = batch succeeded)
    # Raise an exception = batch failed (SQS retries)