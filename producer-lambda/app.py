import boto3
import json
import uuid
import os

sqs = boto3.client("sqs")

QUEUE_URL = os.environ.get("QUEUE_URL")


def lambda_handler(event, context):
    user_id = str(uuid.uuid4())
    name = "Push Push Push" + user_id.split("-")[-1]
    data = {"user_id": user_id, "name": name, "action": "create"}

    sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=json.dumps(data),
        MessageGroupId="group-1",
        MessageDeduplicationId=user_id,
    )

    return {"statusCode": 200, "body": "Message sent"}
