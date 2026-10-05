import json
import boto3
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('StudentsTable')

def lambda_handler(event, context):

    # Get S3 details
    bucket = event['Records'][0]['s3']['bucket']['name']
    object_key = event['Records'][0]['s3']['object']['key']

    # Store metadata in DynamoDB
    table.put_item(
        Item={
            'student_id': str(uuid.uuid4()),
            'name': object_key,
            'email': 'uploaded@wandaprep.com',
            'course': 'S3 Trigger',
            'source_bucket': bucket
        }
    )

    return {
        'statusCode': 200,
        'message': 'S3 event processed and stored in DynamoDB',
        'file_uploaded': object_key
    }
