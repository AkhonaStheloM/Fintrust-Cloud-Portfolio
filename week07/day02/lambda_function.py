import json
import logging
import os

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # event: dict containing the trigger payload
    # context: object with runtime metadata

    logger.info('Event: %s', json.dumps(event))
    logger.info('Function name: %s', context.function_name)
    logger.info('Remaining time (ms): %s', context.get_remaining_time_in_millis())

    # Always return a dict for API Gateway proxy integration
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'ok'})
    }