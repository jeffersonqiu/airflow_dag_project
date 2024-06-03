import json
import boto3
import pandas as pd

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    # TODO implement
    ori_bucket_name = event['Records'][0]['s3']['bucket']['name']
    ori_key = event['Records'][0]['s3']['object']['key']
    
    waiter = s3_client.get_waiter('object_exists')
    waiter.wait(Bucket=ori_bucket_name, Key=ori_key)
    
    response = s3_client.get_object(Bucket=ori_bucket_name, Key=ori_key)
    data = response['Body'].read().decode('utf-8')
    json_data = json.loads(data)
    
    f = []
    for i in json_data["results"]:
        f.append(i)
    df = pd.DataFrame(f)
    # Select specific columns
    selected_columns = ['bathrooms', 'bedrooms', 'city', 'homeStatus', 
                    'homeType','livingArea','price', 'rentZestimate','zipcode']
    df = df[selected_columns]
    
    # Convert DataFrame to CSV format
    csv_data = df.to_csv(index=False)
    
    target_location = "jqiu-transformed-data-zone-first-dag-project"
    target_file_name = ori_key[:-5]
    
    # Upload CSV to S3
    target_key = f"{target_file_name}.csv"
    s3_client.put_object(Bucket=target_location, Key=target_key, Body=csv_data)
        
    return {
        'statusCode': 200,
        'body': json.dumps('Succesfully convert to csv and upload to final S3!')
    }
