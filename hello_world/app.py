import boto3
import os
import uuid
from urllib.parse import unquote_plus
from PIL import Image

s3_client = boto3.client('s3')
SIZE = (304, 228)

def resize_image(image_path, resized_path):
    with Image.open(image_path) as image:
        image.thumbnail(SIZE)
        image.save(resized_path)

def lambda_handler(event, context):
    for record in event['Records']:
        bucket_name = record['s3']['bucket']['name'] # example: energy_market_procesing
        key = unquote_plus(record['s3']['object']['key']) # example: market/zone1/data.csv        
        tmpkey = key.replace('/', '')
        download_path = '/tmp/{}{}'.format(uuid.uuid4(), tmpkey)
        upload_path = '/tmp/resized-{}'.format(tmpkey)
        s3_client.download_file(bucket_name, key, download_path)
        resize_image(download_path, upload_path)
        s3_client.upload_file(upload_path, os.environ["EndBucketName"], key)