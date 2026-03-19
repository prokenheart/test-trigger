import boto3
from datetime import datetime
from aws_lambda_powertools import Logger
import json

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("user")

logger = Logger(service="my_service", level="INFO")


def get_all_users():
    try:
        items = []
        response = table.scan()

        items.extend(response.get("Items", []))

        # Handle pagination
        while "LastEvaluatedKey" in response:
            response = table.scan(ExclusiveStartKey=response["LastEvaluatedKey"])
            items.extend(response.get("Items", []))

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"message": "Success", "data": items}),
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"message": str(e)}),
        }


def create_user(event):
    try:
        body = json.loads(event.get("body") or "{}")

        user_id = body.get("user_id")
        name = body.get("name")

        now = datetime.now().isoformat()
        table.put_item(Item={"user_id": user_id, "updated_at": now, "name": name})
        return {
            "statusCode": 201,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"message": "User created successfully"}),
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"message": str(e)}),
        }


@logger.inject_lambda_context(log_event=True)
def lambda_handler(event, context):
    path = event.get("path")
    method = event.get("httpMethod")

    if path == "/users" and method == "GET":
        return get_all_users()
    elif path == "/users" and method == "POST":
        return create_user(event)
