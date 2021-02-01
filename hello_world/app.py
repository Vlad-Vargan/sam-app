import boto3
import os
import sys
import uuid
from urllib.parse import unquote_plus
from PIL import Image
import PIL.Image


s3_client = boto3.client(
                's3',
                aws_access_key_id='AKIAZIJQ6NNTVC67DXBA',
                aws_secret_access_key='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',
                region_name='eu-central-1'
)

def resize_image(image_path, resized_path):
    with Image.open(image_path) as image:
        image.thumbnail((304, 228))
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
        s3_client.upload_file(upload_path, bucket_name, key)