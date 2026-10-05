import json
import boto3

s3 = boto3.client('s3')
ec2 = boto3.client('ec2')
cloudtrail = boto3.client('cloudtrail')

def lambda_handler(event, context):
    detail = event['detail']
    rule = detail['configRuleName']
    resource = detail['resourceId']

    if rule.startswith("s3-bucket-public"):
        s3.put_public_access_block(
            Bucket=resource,
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': True,
                'IgnorePublicAcls': True,
                'BlockPublicPolicy': True,
                'RestrictPublicBuckets': True
            }
        )

    elif rule == "encrypted-volumes":
        ec2.create_tags(
            Resources=[resource],
            Tags=[{'Key': 'EncryptionViolation', 'Value': 'true'}]
        )

    elif rule == "restricted-common-ports":
        # Example: notify only (safe for teaching)
        print(f"Security Group violation: {resource}")

    elif rule == "cloudtrail-enabled":
        trails = cloudtrail.describe_trails()['trailList']
        for t in trails:
            cloudtrail.start_logging(Name=t['Name'])

    return {"status": "processed"}
