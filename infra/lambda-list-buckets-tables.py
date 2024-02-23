# used for https://lytx.atlassian.net/browse/COST-46 testing
import boto3
def lambda_handler(event, context):
    # Create clients for DynamoDB and S3
    dynamodb_client = boto3.client('dynamodb')
    s3_client = boto3.client('s3')
    # List DynamoDB tables
    dynamodb_response = dynamodb_client.list_tables()
    dynamodb_table_names = dynamodb_response.get('TableNames', [])
    # List S3 buckets
    s3_response = s3_client.list_buckets()
    s3_bucket_names = [bucket['Name'] for bucket in s3_response.get('Buckets', [])]
    # Print the list of DynamoDB tables
    print("DynamoDB Tables:")
    for table_name in dynamodb_table_names:
        print(table_name)
    # Print the list of S3 buckets
    print("\nS3 Buckets:")
    for bucket_name in s3_bucket_names:
        print(bucket_name)
    # You can also return the table and bucket names if needed
    return {
        'statusCode': 200,
        'body': {
            'DynamoDBTables': dynamodb_table_names,
            'S3Buckets': s3_bucket_names
        }
    }

