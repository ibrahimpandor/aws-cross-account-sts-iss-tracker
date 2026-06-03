import json
import boto3
import urllib.request
from datetime import datetime

def lambda_handler(event, context):
    # Step 1: ISS location from public API
    url = "https://api.wheretheiss.at/v1/satellites/25544"
    with urllib.request.urlopen(url) as response:
        iss_data = json.loads(response.read().decode())
    
    # Add timestamp
    iss_data['retrieved_at'] = datetime.utcnow().isoformat()
    
    # Step 2: Assume role in Account B done through STS
    sts_client = boto3.client('sts')
    assumed_role = sts_client.assume_role(
        RoleArn="arn:aws:iam::160184161780:role/iss-tracker-cross-account-role",
        RoleSessionName="ISSTrackerSession"
    )
    
    # Step 3: Use temporary credentials to link and connect to Account B's S3 bucket
    credentials = assumed_role['Credentials']
    s3_client = boto3.client(
        's3',
        aws_access_key_id=credentials['AccessKeyId'],
        aws_secret_access_key=credentials['SecretAccessKey'],
        aws_session_token=credentials['SessionToken']
    )
    
    # Step 4: Write ISS data to S3 bucket in Account B
    timestamp = datetime.utcnow().strftime('%Y/%m/%d/%H-%M-%S')
    key = f"iss-data/{timestamp}.json"
    
    s3_client.put_object(
        Bucket="iss-tracker-data-bucket",
        Key=key,
        Body=json.dumps(iss_data),
        ContentType="application/json"
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps(f"ISS data written to s3://iss-tracker-data-bucket/{key}")
    }
