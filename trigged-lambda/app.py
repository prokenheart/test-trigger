def lambda_handler(event, context):

    for record in event["Records"]:
        event_name = record["eventName"]  # INSERT | MODIFY | REMOVE

        if event_name == "INSERT":
            new_image = record["dynamodb"]["NewImage"]
            print("New item:", new_image)

        elif event_name == "MODIFY":
            old_image = record["dynamodb"]["OldImage"]
            new_image = record["dynamodb"]["NewImage"]
            print("Updated:", old_image, "->", new_image)

        elif event_name == "REMOVE":
            old_image = record["dynamodb"]["OldImage"]
            print("Deleted:", old_image)


# event = {
#     "Records": [
#         {
#             "eventID": "1",
#             "eventName": "INSERT",
#             "dynamodb": {
#                 "Keys": {
#                     "user_id": {"S": "2"},
#                     "updated_at": {"S": "2026-03-18T14:48:30+07:00"},
#                 },
#                 "NewImage": {
#                     "user_id": {"S": "2"},
#                     "updated_at": {"S": "2026-03-18T14:48:30+07:00"},
#                     "name": {"S": "Proken Heart"},
#                 },
#             },
#         },
#     ]
# }


# if __name__ == "__main__":
#     lambda_handler(event, None)
