import boto3
import json

lambda_client = boto3.client("lambda")


def lambda_handler(event, context):
    response = lambda_client.invoke(
        FunctionName="producer-function", InvocationType="RequestResponse"
    )

    result = json.loads(response["Payload"].read())

    return {"statusCode": 200, "body": json.dumps(result)}
