import boto3
from datetime import date, timedelta

ce = boto3.client('ce', region_name='us-east-1')

def get_monthly_spend_by_service(year, month):
    """
    Returns dict mapping service name to total spend (USD) for the given month.
    """
    start = f'{year}-{month:02d}-01'
    # Compute first day of next month
    if month == 12:
        end = f'{year + 1}-01-01'
    else:
        end = f'{year}-{month + 1:02d}-01'

    response = ce.get_cost_and_usage(
        TimePeriod={'Start': start, 'End': end},
        Granularity='MONTHLY',
        Metrics=['UnblendedCost'],
        GroupBy=[{'Type': 'DIMENSION', 'Key': 'SERVICE'}]
    )

    results = {}
    for group in response['ResultsByTime'][0]['Groups']:
        service = group['Keys'][0]
        cost = float(group['Metrics']['UnblendedCost']['Amount'])
        if cost > 0.01:  # filter out near-zero services
            results[service] = round(cost, 2)

    return dict(sorted(results.items(), key=lambda x: x[1], reverse=True))

spend = get_monthly_spend_by_service(2024, 6)
for service, cost in list(spend.items())[:10]:
    print(f'  {service:<45} ${cost:>10,.2f}')