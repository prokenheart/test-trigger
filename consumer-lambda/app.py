import boto3
from datetime import datetime
import json
from aws_lambda_powertools import Logger

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("user")

logger = Logger(service="sqs_consumer", level="INFO")


def process_user_message(message_body):
    try:
        body = json.loads(message_body)
        user_id = body.get("user_id")
        name = body.get("name")
        action = body.get("action", "create").lower()

        now = datetime.now().isoformat()

        if action == "create":
            table.put_item(Item={"user_id": user_id, "name": name, "updated_at": now})
            logger.info(f"[CREATE] User {user_id} created: {name}")
        elif action == "update":
            table.update_item(
                Key={"user_id": user_id},
                UpdateExpression="SET #n = :name, updated_at = :updated",
                ExpressionAttributeNames={"#n": "name"},
                ExpressionAttributeValues={":name": name, ":updated": now},
            )
            logger.info(f"[UPDATE] User {user_id} updated to: {name}")
        elif action == "delete":
            table.delete_item(Key={"user_id": user_id})
            logger.info(f"[DELETE] User {user_id} deleted")
        else:
            logger.warning(f"[SKIP] Unknown action '{action}' for user {user_id}")
            return False

        return True

    except Exception as e:
        logger.exception(f"Failed to process message: {message_body}. Error: {e}")
        return False


@logger.inject_lambda_context(log_event=True)
def lambda_handler(event, context):
    success_count = 0
    failure_count = 0

    for record in event.get("Records", []):
        body = record.get("body")
        if process_user_message(body):
            success_count += 1
        else:
            failure_count += 1

    summary = {
        "message": "SQS processing finished",
        "success": success_count,
        "failure": failure_count
    }

    logger.info(f"Summary: {summary}")

    
    return {
        "statusCode": 200,
        "body": json.dumps(summary)
    }