import boto3, json

pricing = boto3.client('pricing', region_name='us-east-1')

def get_ec2_ondemand_price(instance_type, region='af-south-1', os='Linux'):
    """
    Returns hourly On-Demand price for an EC2 instance type in USD.
    """
    # AWS uses long region names in Pricing API
    region_names = {
        'af-south-1': 'Africa (Cape Town)',
        'eu-west-1':  'Europe (Ireland)',
        'us-east-1':  'US East (N. Virginia)',
    }

    response = pricing.get_products(
        ServiceCode='AmazonEC2',
        Filters=[
            {'Type': 'TERM_MATCH', 'Field': 'instanceType',    'Value': instance_type},
            {'Type': 'TERM_MATCH', 'Field': 'location',        'Value': region_names[region]},
            {'Type': 'TERM_MATCH', 'Field': 'operatingSystem', 'Value': os},
            {'Type': 'TERM_MATCH', 'Field': 'tenancy',         'Value': 'Shared'},
            {'Type': 'TERM_MATCH', 'Field': 'preInstalledSw',  'Value': 'NA'},
            {'Type': 'TERM_MATCH', 'Field': 'capacityStatus',  'Value': 'Used'},
        ],
        MaxResults=1
    )

    if not response['PriceList']:
        return None

    product = json.loads(response['PriceList'][0])
    # Navigate the nested price structure
    terms = product['terms']['OnDemand']
    price_dimensions = next(iter(next(iter(terms.values()))['priceDimensions'].values()))
    price_usd = float(price_dimensions['pricePerUnit']['USD'])
    return price_usd

# Test with FinTrust instance types
instances = ['m5.xlarge', 'r5.2xlarge', 'c5.large']
for inst in instances:
    price = get_ec2_ondemand_price(inst, region='af-south-1')
    if price:
        print(f'{inst}: ${price:.4f}/hr = ${price * 730:.2f}/month')
    else:
        print(f'{inst}: price not found for af-south-1')