import json
import boto3
import os
import uuid
import base64
from io import BytesIO
from requests_toolbelt.multipart import decoder

s3 = boto3.client("s3")
stepfunctions = boto3.client("stepfunctions")

UPLOAD_BUCKET = os.environ.get("UPLOAD_BUCKET")
STATE_MACHINE_ARN = os.environ.get("STATE_MACHINE_ARN")

def lambda_handler(event, context):
    print("Event received:", json.dumps(event))

    # === API Gateway Flow ===
    if "body" in event and "headers" in event:
        try:
            print("UPLOAD_BUCKET:", UPLOAD_BUCKET)
            print("STATE_MACHINE_ARN:", STATE_MACHINE_ARN)

            headers = event.get("headers") or {}
            content_type = headers.get("Content-Type") or headers.get("content-type")
            print("Raw Content-Type:", content_type)
            print("Headers received:", headers)
            print("isBase64Encoded:", event.get("isBase64Encoded", False))
            print("Body type:", type(event.get("body")))

            if not content_type:
                raise ValueError("Missing Content-Type header")

            if event.get("isBase64Encoded", False):
                body = base64.b64decode(event["body"])
            else:
                body = event["body"].encode("utf-8")

            multipart_data = decoder.MultipartDecoder(body, content_type)

            file_bytes = None
            file_type = "image/jpeg"

            for part in multipart_data.parts:
                content_disposition = part.headers.get(b"Content-Disposition", b"").decode(errors="ignore")
                print("Part headers:", content_disposition)
                if "filename=" in content_disposition:
                    file_bytes = part.content
                    file_type = part.headers.get(b"Content-Type", b"image/jpeg").decode()
                    break

            if not file_bytes:
                raise ValueError("No file found in multipart upload")

            image_id = str(uuid.uuid4())
            s3_key = f"uploads/{image_id}.jpg"

            s3.put_object(
                Bucket=UPLOAD_BUCKET,
                Key=s3_key,
                Body=file_bytes,
                ContentType=file_type
            )

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

    return {
        "statusCode": 400,
        "body": json.dumps({"error": "Unsupported event format"})
    }