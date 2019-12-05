import boto3
import pandas as pd

region = "eu-west-1"
s3_client = boto3.client('s3', region_name=region)
location = {'LocationConstraint': region }

bucket = "blossom-data-eng-omar-maj"

# 
data = pd.read_csv('data/free-7-million-company-dataset.zip', compression='zip')

data = data[data['domain'].isna()]
data.to_parquet('data/data.parquet')
data.to_json('data/data.json.gz', orient='records', 
            lines=True, compression='gzip')

s3_client.upload_file("data/data.json.gz", bucket, "data.json.gz")
s3_client.upload_file("data/data.parquet", bucket, "data.parquet")



