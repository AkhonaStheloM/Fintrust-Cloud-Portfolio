import boto3, json

budgets = boto3.client('budgets', region_name='us-east-1')
ACCOUNT_ID = boto3.client('sts').get_caller_identity()['Account']

def create_monthly_budget(budget_name, limit_usd, alert_pct, email):
    """Create a monthly cost budget with a single percentage-threshold alert."""
    budgets.create_budget(
        AccountId=ACCOUNT_ID,
        Budget={
            'BudgetName': budget_name,
            'BudgetLimit': {'Amount': str(limit_usd), 'Unit': 'USD'},
            'TimeUnit': 'MONTHLY',
            'BudgetType': 'COST',
        },
        NotificationsWithSubscribers=[{
            'Notification': {
                'NotificationType': 'ACTUAL',
                'ComparisonOperator': 'GREATER_THAN',
                'Threshold': alert_pct,
                'ThresholdType': 'PERCENTAGE',
            },
            'Subscribers': [{'SubscriptionType': 'EMAIL', 'Address': email}]
        }]
    )
    print(f'Budget "{budget_name}" created: ${limit_usd}/month, alert at {alert_pct}%')

# FinTrust: create a budget for the Analytics team account
create_monthly_budget(
    budget_name='FinTrust-Analytics-Monthly',
    limit_usd=15000,
    alert_pct=80.0,
    email='analytics-lead@fintrust.co.za'
)

# List all budgets and show current utilisation
response = budgets.describe_budgets(AccountId=ACCOUNT_ID)
for b in response['Budgets']:
    limit  = float(b['BudgetLimit']['Amount'])
    actual = float(b.get('CalculatedSpend', {}).get('ActualSpend', {}).get('Amount', 0))
    pct = (actual / limit * 100) if limit > 0 else 0
    print(f'{b["BudgetName"]}: ${actual:.2f} / ${limit:.2f} ({pct:.1f}%)')