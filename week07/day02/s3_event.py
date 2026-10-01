def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key    = record['s3']['object']['key']
        size   = record['s3']['object']['size']

        logger.info('New file: s3://%s/%s (%d bytes)', bucket, key, size)