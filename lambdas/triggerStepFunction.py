import json
import boto3
import os
import uuid
import base64
import cgi
from io import BytesIO

s3 = boto3.client("s3")
stepfunctions = boto3.client("stepfunctions")

UPLOAD_BUCKET = os.environ.get("UPLOAD_BUCKET")
STATE_MACHINE_ARN = os.environ.get("STATE_MACHINE_ARN")

def lambda_handler(event, context):
    print("Event received:", json.dumps(event))

    # API Gateway flow (POST /upload)
    if "body" in event and "headers" in event:
        try:
            body = base64.b64decode(event["body"])
            content_type = event["headers"].get("Content-Type") or event["headers"].get("content-type")

            environ = {'REQUEST_METHOD': 'POST'}
            headers = {'content-type': content_type}
            fs = cgi.FieldStorage(fp=BytesIO(body), environ=environ, headers=headers)

            file_item = fs['file']
            file_bytes = file_item.file.read()
            file_type = file_item.type or "image/jpeg"

            # Unique key for S3
            image_id = str(uuid.uuid4())
            s3_key = f"uploads/{image_id}.jpg"

            # Upload to S3
            s3.put_object(
                Bucket=UPLOAD_BUCKET,
                Key=s3_key,
                Body=file_bytes,
                ContentType=file_type
            )

            # Start Step Function
            stepfunctions.start_execution(
                stateMachineArn=STATE_MACHINE_ARN,
                input=json.dumps({
                    "bucket": UPLOAD_BUCKET,
                    "key": s3_key,
                    "imageId": image_id
                })
            )

            return {
                "statusCode": 200,
                "headers": {"Access-Control-Allow-Origin": "*"},
                "body": json.dumps({
                    "message": "Image uploaded and Step Function started",
                    "imageId": image_id
                })
            }

        except Exception as e:
            print("Upload error:", str(e))
            return {
                "statusCode": 500,
                "headers": {"Access-Control-Allow-Origin": "*"},
                "body": json.dumps({"error": str(e)})
            }

    # ✅ S3-triggered event (existing behavior)
    elif "Records" in event and event["Records"][0]["eventSource"] == "aws:s3":
        try:
            record = event['Records'][0]
            bucket = record['s3']['bucket']['name']
            key = record['s3']['object']['key']

            input_data = {
                "bucket": bucket,
                "key": key,
                "imageId": key.split("/")[-1].split(".")[0]
            }

            stepfunctions.start_execution(
                stateMachineArn=STATE_MACHINE_ARN,
                input=json.dumps(input_data)
            )

            return {
                "statusCode": 200,
                "body": json.dumps("Step Function started from S3 event")
            }

        except Exception as e:
            print("S3 event error:", str(e))
            return {
                "statusCode": 500,
                "body": json.dumps({"error": str(e)})
            }

    return {
        "statusCode": 400,
        "body": json.dumps({"error": "Unsupported event format"})
    }