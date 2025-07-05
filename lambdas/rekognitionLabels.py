import json
import boto3

rekognition = boto3.client('rekognition')
s3 = boto3.client('s3')

def lambda_handler(event, context):
    print("Event received:", json.dumps(event))

    bucket = event['bucket']
    key = event['key']
    image_id = event['imageId']

    # Call Amazon Rekognition to detect labels
    response = rekognition.detect_labels(
        Image={
            'S3Object': {
                'Bucket': bucket,
                'Name': key
            }
        },
        MaxLabels=10,
        MinConfidence=70
    )

    labels = [
        {
            "Name": label['Name'],
            "Confidence": round(label['Confidence'], 2)
        }
        for label in response['Labels']
    ]

    print(f"Labels detected: {labels}")

    return {
        "bucket": bucket,
        "key": key,
        "imageId": image_id,
        "labels": labels
    }