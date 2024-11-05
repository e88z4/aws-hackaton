import boto3
import json
import uuid
import sys

# Initialize boto3 clients
dynamodb = boto3.client('dynamodb')
s3 = boto3.client('s3')

# DynamoDB table and S3 bucket names
DYNAMODB_TABLE = 'Providers'
S3_BUCKET = 'product-review-files-20241104'

# Get the file path from the user input
file_path = input("Enter the path to the JSON file: ")

# Load JSON data
with open(file_path) as f:
    providers = json.load(f)

for provider in providers:
    provider_id = str(uuid.uuid4())
    
    # Prepare provider data for DynamoDB
    provider_item = {
        'ProviderID': {'S': provider_id},
        'ProviderName': {'S': provider['provider_name']},
        'ProviderType': {'S': provider['provider_type']},
        'ProviderAddress': {'S': provider['provider_address']},
        'AreaCode': {'S': provider['area_code']},
        'PhoneNumber': {'S': provider['phone_number']}
    }
    
    # Put provider data into DynamoDB
    dynamodb.put_item(TableName=DYNAMODB_TABLE, Item=provider_item)
    
    # Store each review in S3
    for review in provider['reviews']:
        review_id = str(uuid.uuid4())
        review_object = {
            'reviewer_name': review['reviewer_name'],
            'reviewer_datetime': review['reviewer_datetime'],
            'text': review['text']
        }
        
        # Put review object into S3
        s3.put_object(
            Bucket=S3_BUCKET,
            Key=f'{provider_id}/{review_id}.json',
            Body=json.dumps(review_object)
        )

print("Data loaded successfully.")