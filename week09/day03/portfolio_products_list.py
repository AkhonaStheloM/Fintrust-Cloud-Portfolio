import boto3

sc = boto3.client('servicecatalog', region_name='af-south-1')

# Collect portfolios from both sources
portfolios = sc.list_accepted_portfolio_shares()['PortfolioDetails']
own        = sc.list_portfolios()['PortfolioDetails']
all_portfolios = {p['Id']: p for p in portfolios + own}

for pid, portfolio in all_portfolios.items():
    print(f'\nPortfolio: {portfolio["DisplayName"]} ({pid})')

    # List products in this portfolio
    products = sc.search_products_as_admin(
        PortfolioId=pid
    )['ProductViewDetails']

    for pv in products:
        p = pv['ProductViewSummary']
        print(f'  Product: {p["Name"]} | Type: {p["Type"]} | Owner: {p["Owner"]}')

# Provision a product (simulate — do not run without a real product id)
# response = sc.provision_product(
#     ProductId='prod-xxxxxxxxxxxx',
#     ProvisioningArtifactId='pa-xxxxxxxxxxxx',
#     ProvisionedProductName='fintrust-analytics-stack-001',
#     ProvisioningParameters=[
#         {'Key': 'CostCentre', 'Value': 'Analytics'},
#         {'Key': 'Team', 'Value': 'DataEngineering'},
#     ]
# )