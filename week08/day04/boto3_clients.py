import boto3

# Rekognition client — image analysis and face comparison
rek = boto3.client('rekognition', region_name='af-south-1')

# Comprehend client — NLP: PII detection, sentiment, entity recognition
comp = boto3.client('comprehend', region_name='af-south-1')