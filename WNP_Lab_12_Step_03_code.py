import json
import boto3

s3 = boto3.client('s3')
sns = boto3.client('sns')

SNS_TOPIC_ARN = "arn:aws:sns:<region>:<account-id>:security-publicbucket-alerts"

def handler(event, context):
    print("Event Received:", json.dumps(event))

    detail = event['detail']
    bucket = detail['requestParameters']['bucketName']

    # ----- 1. Enable Block Public Access -----
    s3.put_public_access_block(
        Bucket=bucket,
        PublicAccessBlockConfiguration={
            "BlockPublicAcls": True,
            "IgnorePublicAcls": True,
            "BlockPublicPolicy": True,
            "RestrictPublicBuckets": True
        }
    )

    # ----- 2. Remove any public ACLs -----
    try:
        s3.put_bucket_acl(Bucket=bucket, ACL="private")
    except Exception as e:
        print("ACL update error:", e)

    # ----- 3. Tag bucket to mark auto-fix -----
    s3.put_bucket_tagging(
        Bucket=bucket,
        Tagging={
            'TagSet': [
                {'Key': 'SecurityAutoFix', 'Value': 'True'},
                {'Key': 'FixedBy', 'Value': 'Lambda'}
            ]
        }
    )

    # ----- 4. Send notification -----
    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject="⚠ Public Bucket Auto-Fixed",
        Message=f"The bucket '{bucket}' was public and has been automatically secured."
    )

    return {"status": "success", "bucket": bucket}

