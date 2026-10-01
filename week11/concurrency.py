from concurrent.futures import ThreadPoolExecutor, as_completed
import boto3

s3 = boto3.client('s3')

def get_object_metadata(bucket: str, key: str) -> dict:
    """Fetch S3 object metadata — I/O bound, ideal for threading."""
    response = s3.head_object(Bucket=bucket, Key=key)
    return {'key': key, 'size': response['ContentLength']}

keys = ['data/file1.csv', 'data/file2.csv', 'data/file3.csv']  # ... 50 keys
bucket = 'fintrust-raw-data'

# Sequential: ~50 × 100ms = 5 seconds
# Concurrent: ~max(100ms per thread) ≈ 200ms with 32 workers
results = []
with ThreadPoolExecutor(max_workers=32) as executor:
    futures = {
        executor.submit(get_object_metadata, bucket, key): key
        for key in keys
    }
    for future in as_completed(futures):
        try:
            results.append(future.result())
        except Exception as e:
            print(f"Failed for {futures[future]}: {e}")
            
