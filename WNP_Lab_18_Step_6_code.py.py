import json
import boto3
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('StudentsTable')

def lambda_handler(event, context):

    # Example manual insert
    table.put_item(
        Item={
            'student_id': str(uuid.uuid4()),
            'name': 'Lambda User',
            'email': 'lambda@wandaprep.com',
            'course': 'Serverless'
        }
    )

    # Read existing record
    response = table.get_item(
        Key={'student_id': '1001'}
    )

    return {
        'statusCode': 200,
        'message': 'Lambda wrote and read from DynamoDB',
        'existing_student': response.get('Item')
    }
