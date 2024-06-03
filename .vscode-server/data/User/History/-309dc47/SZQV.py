import json
import boto3

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    # TODO implement
    ori_bucket_name = event['Records'][0]['s3']['bucket']['name']
    ori_key = event['Records'][0]['s3']['object']['key']
    
    # print(ori_bucket_name, ori_key)

    waiter = s3_client.get_waiter('object_exists')
    waiter.wait(Bucket=ori_bucket_name, Key=ori_key)
    
    target_location = "jqiu-intermediate-zone-first-dag-project"
    copy_source = {
        'Bucket': ori_bucket_name,
        'Key': ori_key
    }

    s3_client.copy(
        CopySource=copy_source, 
        Bucket='jqiu-intermediate-zone-first-dag-project',
        Key=ori_key
    )
        
    return {
        'statusCode': 200,
        'body': json.dumps('Succesfully copy file from landing to intermediate S3 bucket!')
    }
