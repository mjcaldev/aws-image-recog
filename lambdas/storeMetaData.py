import json
import boto3
import os
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
sns = boto3.client('sns')

table_name = os.environ.get("TABLE_NAME")
topic_arn = os.environ.get("TOPIC_ARN")  # Optional, if you decide to pass this in too

def lambda_handler(event, context):
    print("Event received:", json.dumps(event))

    bucket = event['bucket']
    key = event['key']
    image_id = event['imageId']
    labels = event.get('labels', [])

    # Insert into DynamoDB
    table = dynamodb.Table(table_name)

    table.put_item(
        Item={
            "imageId": image_id,
            "s3Path": f"s3://{bucket}/{key}",
            "labels": labels,
            "timestamp": datetime.utcnow().isoformat()
        }
    )

    print(f"Metadata stored for imageId: {image_id}")

    # Optional: send SNS or SES notification
    if topic_arn:
        sns.publish(
            TopicArn=topic_arn,
            Subject="Image Processed",
            Message=f"Your image '{image_id}' was processed and labeled successfully."
        )
        print("Notification sent.")

    return {
        "status": "SUCCESS",
        "imageId": image_id,
        "labels": labels
    }