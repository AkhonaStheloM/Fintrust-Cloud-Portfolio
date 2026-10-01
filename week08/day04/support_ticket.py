import boto3, json

sqs = boto3.client('sqs', region_name='af-south-1')
comp = boto3.client('comprehend', region_name='af-south-1')

URGENT_QUEUE_URL = 'https://sqs.af-south-1.amazonaws.com/ACCOUNT_ID/fintrust-support-urgent'
STANDARD_QUEUE_URL = 'https://sqs.af-south-1.amazonaws.com/ACCOUNT_ID/fintrust-support-standard'

def process_support_ticket(ticket_text):
    # Step 1: redact PII
    redacted_text, pii_types = redact_pii(ticket_text)

    # Step 2: detect sentiment on the original text
    sentiment_resp = comp.detect_sentiment(Text=ticket_text, LanguageCode='en')
    sentiment = sentiment_resp['Sentiment']

    # Step 3: route to appropriate queue
    queue_url = URGENT_QUEUE_URL if sentiment == 'NEGATIVE' else STANDARD_QUEUE_URL

    message = {
        'redacted_text': redacted_text,
        'sentiment': sentiment,
        'pii_types_found': pii_types,
        'priority': 'HIGH' if sentiment == 'NEGATIVE' else 'STANDARD'
    }

    sqs.send_message(QueueUrl=queue_url, MessageBody=json.dumps(message))

    return message