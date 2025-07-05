import json
import boto3
import os
from PIL import Image

s3 = boto3.client('s3')

def lambda_handler(event, context):
    print("Event received:", json.dumps(event))

    bucket = event['bucket']
    key = event['key']
    image_id = event['imageId']

    # Create temp paths
    download_path = f"/tmp/{image_id}-original.jpg"
    resized_path = f"/tmp/{image_id}-resized.jpg"

    # Download original image from S3
    s3.download_file(bucket, key, download_path)

    # Resize the image using Pillow
    with Image.open(download_path) as img:
        img = img.convert("RGB")  # Ensure consistent format
        img.thumbnail((512, 512))  # Resize keeping aspect ratio
        img.save(resized_path, format="JPEG")

    # Upload resized image to a 'processed/' folder
    resized_key = f"processed/{image_id}-resized.jpg"
    s3.upload_file(resized_path, bucket, resized_key)

    print(f"Resized image saved to {resized_key}")

    return {
        "bucket": bucket,
        "key": resized_key,
        "imageId": image_id
    }