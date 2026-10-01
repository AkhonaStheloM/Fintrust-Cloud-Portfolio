import boto3, json
from collections import defaultdict

tagging = boto3.client('resourcegroupstaggingapi', region_name='af-south-1')

REQUIRED_TAGS = ['CostCentre', 'Team', 'Environment']

def audit_tag_compliance():
    """
    Scan all tagged resources in the account and identify those
    missing one or more required tags.
    Returns: dict mapping resource ARN to list of missing tags.
    """
    non_compliant = {}
    paginator = tagging.get_paginator('get_resources')

    for page in paginator.paginate():
        for resource in page['ResourceTagMappingList']:
            arn = resource['ResourceARN']
            existing_keys = {t['Key'] for t in resource.get('Tags', [])}
            missing = [tag for tag in REQUIRED_TAGS if tag not in existing_keys]
            if missing:
                non_compliant[arn] = missing

    return non_compliant

violations = audit_tag_compliance()
print(f'Non-compliant resources: {len(violations)}')

# Group by resource type (extracted from ARN)
by_type = defaultdict(list)
for arn, missing in violations.items():
    # arn format: arn:aws:service:region:account:resource-type/name
    parts = arn.split(':')
    service = parts[2] if len(parts) > 2 else 'unknown'
    by_type[service].append((arn, missing))

for service, items in sorted(by_type.items()):
    print(f'\n  {service.upper()} ({len(items)} violations):')
    for arn, missing in items[:3]:  # show first 3 per service
        short_arn = '...' + arn[-40:]
        print(f'    {short_arn} — missing: {", ".join(missing)}')