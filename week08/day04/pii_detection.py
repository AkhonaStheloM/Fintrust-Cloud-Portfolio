import boto3

comp = boto3.client('comprehend', region_name='af-south-1')

def redact_pii(text):
    """
    Detect and redact PII from support ticket text.
    Returns redacted text and list of detected PII types.
    """
    response = comp.detect_pii_entities(Text=text, LanguageCode='en')
    entities = response['Entities']

    # Sort descending by position so replacements don't shift offsets
    entities.sort(key=lambda e: e['BeginOffset'], reverse=True)

    detected_types = list({e['Type'] for e in entities})
    text_chars = list(text)

    for entity in entities:
        replacement = f'[{entity["Type"]}]'
        text_chars[entity['BeginOffset']:entity['EndOffset']] = list(replacement)

    return ''.join(text_chars), detected_types

# Test with a sample support ticket
ticket = (
    "My name is Sipho Nkosi and my account number is ACC-7823041. "
    "My ID number is 9203045678082. I contacted you from 083 555 1234. "
    "Please help me reset my PIN."
)

redacted, pii_types = redact_pii(ticket)
print('Original:', ticket)
print('Redacted:', redacted)
print('PII found:', pii_types)