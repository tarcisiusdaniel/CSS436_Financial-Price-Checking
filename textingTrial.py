import boto3

sns_client = boto3.client(
    'sns',
    aws_access_key_id='AKIA3X5E4PGQKNS35RGT',
    aws_secret_access_key='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',
    region_name = 'us-west-2',
)
tarc = '+12066378356'
sns_client.publish(PhoneNumber = tarc, Message = 'test')