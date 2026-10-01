import boto3, json

rek = boto3.client('rekognition', region_name='af-south-1')

def kyc_verify(selfie_bucket, selfie_key, id_bucket, id_key, threshold=95.0):
    """
    Compare a selfie to the ID document photo.
    Returns dict with match (bool), similarity (float), and decision.
    """
    response = rek.compare_faces(
        SourceImage={'S3Object': {'Bucket': selfie_bucket, 'Name': selfie_key}},
        TargetImage={'S3Object': {'Bucket': id_bucket, 'Name': id_key}},
        SimilarityThreshold=threshold
    )

    if not response['FaceMatches']:
        return {
            'match': False,
            'similarity': 0.0,
            'decision': 'REJECT',
            'reason': 'No face match found'
        }

    top_match = response['FaceMatches'][0]
    similarity = top_match['Similarity']

    return {
        'match': True,
        'similarity': round(similarity, 2),
        'decision': 'APPROVE' if similarity >= threshold else 'MANUAL_REVIEW',
        'reason': f'Face similarity {similarity:.1f}% (threshold {threshold}%)'
    }

# Test (use placeholder keys — replace with real test images)
result = kyc_verify(
    selfie_bucket='fintrust-kyc-uploads', selfie_key='customers/ACC-0001/selfie.jpg',
    id_bucket='fintrust-kyc-uploads',     id_key='customers/ACC-0001/id_front.jpg'
)
print(json.dumps(result, indent=2))

