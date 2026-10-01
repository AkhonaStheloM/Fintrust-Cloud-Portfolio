from opensearchpy import OpenSearch
import json, datetime

client = OpenSearch(
    hosts=[{'host': 'search-fintrust-security-logs.af-south-1.es.amazonaws.com', 'port': 443}],
    http_auth=('admin', 'CHANGE_ME'),
    use_ssl=True, verify_certs=True
)

# Index a security event document
doc = {
    'timestamp': datetime.datetime.utcnow().isoformat(),
    'event_type': 'SUSPICIOUS_LOGIN',
    'account_id': 'ACC-0001',
    'source_ip': '41.13.45.22',
    'country': 'NG',
    'risk_score': 87
}

index_name = f'fintrust-security-{datetime.date.today().strftime("%Y-%m")}'
response = client.index(index=index_name, body=doc)
print(f'Indexed document: {response["_id"]}')

# Search for high-risk events
query = {'query': {'range': {'risk_score': {'gte': 80}}}}
results = client.search(index=index_name, body=query)
for hit in results['hits']['hits']:
    print(hit['_source'])