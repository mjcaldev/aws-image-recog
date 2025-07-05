import json
import boto3
import os

stepfunctions = boto3.client('stepfunctions')

def lambda_handler(event, context):
    print("Event received:", json.dumps(event))

    # Get the uploaded file info from S3 event
    record = event['Records'][0]
    bucket = record['s3']['bucket']['name']
    key = record['s3']['object']['key']

    # Build the input for the Step Function
    input_data = {
        "bucket": bucket,
        "key": key,
        "imageId": key.split("/")[-1].split(".")[0]  # Strip path and extension
    }

    # Replace with your actual state machine ARN (you can inject via env var)
    state_machine_arn = os.environ.get("STATE_MACHINE_ARN")

    if not state_machine_arn:
        raise ValueError("Missing STATE_MACHINE_ARN environment variable")

    response = stepfunctions.start_execution(
        stateMachineArn=state_machine_arn,
        input=json.dumps(input_data)
    )

    print("Step Function started:", response['executionArn'])

    return {
        "statusCode": 200,
        "body": json.dumps("Step Function started successfully")
    }