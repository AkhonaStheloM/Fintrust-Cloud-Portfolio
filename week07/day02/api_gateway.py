import json 

def lambda_handler(event, context):
    # HTTP method and path
    method = event['httpMethod']        # 'POST', 'GET', etc.
    path   = event['path']              # '/transactions'

    # Query string parameters (may be None)
    params = event.get('queryStringParameters') or {}

    # Request body (always a string in API GW proxy)
    body_str = event.get('body') or '{}'
    body = json.loads(body_str)

    # Headers
    headers = event.get('headers') or {}
    auth_header = headers.get('Authorization', '')

    return {'statusCode': 200, 'body': json.dumps({'received': body})}