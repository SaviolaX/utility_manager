import json
import os

import boto3
from core.db_handler import UtilitiesDB
from core.models import Utility_manager
from core.services import CustomErrorException, DataHandler, response_handler

STATUS_CODE_OK = 200
STATUS_CODE_INTERNAL_SERVER_ERROR = 500
STATUS_CODE_BAD_REQUEST = 400
ACA_ORIGIN = "*"


# db_arn = "arn:aws:dynamodb:eu-central-1:153061395159:table/utility_manager_db"
db_arn = os.environ.get("DYNAMO_DB_TABLE") or ""

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(db_arn)

db = UtilitiesDB(table)


def lambda_handler(event: dict, context: dict) -> dict:

    username = (
        event.get("requestContext")
        .get("authorizer")
        .get("claims")
        .get("cognito:username")
    )

    if event.get("httpMethod") == "GET":
        try:
            resp = db.get_all(user_id=username)
            formatted_data = DataHandler.format_data(resp["Items"])

            return response_handler(
                status_code=STATUS_CODE_OK,
                body=json.dumps(
                    {
                        "utilities_list": formatted_data,
                    }
                ),
            )
        except CustomErrorException as ex:
            return response_handler(
                status_code=STATUS_CODE_BAD_REQUEST,
                body=json.dumps(ex.to_dict()),
            )

    if event.get("httpMethod") == "POST":
        try:
            all_data = db.get_all(user_id=username)

        except CustomErrorException as ex:
            return response_handler(
                status_code=STATUS_CODE_BAD_REQUEST,
                body=json.dumps(ex.to_dict()),
            )
        if all_data["Count"] != 0:
            # Get all needed data
            new_data = json.loads(event["body"])["body"]["payload"]
            old_data = all_data["Items"]

            # Format data
            formatted_old_data = DataHandler.format_data(old_data)
            ordered_list = DataHandler.order_by_date(formatted_old_data, "asc")

            try:
                # Check if the data is valid
                DataHandler.validate_data(new_data)

                # Calculations
                um = Utility_manager.from_json(new_data)
                result = um.calculate_costs(ordered_list[-1])

                # Saving calculations to db
                resp = db.add(
                    p_key=username,
                    s_key=result["date"],
                    utilities=result["utilities"],
                    prices=result["prices"],
                    cost=result["cost"],
                )
            except CustomErrorException as ex:
                return response_handler(
                    status_code=STATUS_CODE_BAD_REQUEST,
                    body=json.dumps(ex.to_dict()),
                )

            return response_handler(
                status_code=STATUS_CODE_OK,
                body=json.dumps(
                    {
                        "message": "New record created.",
                    }
                ),
            )
        else:
            # Get new (first) data
            new_data = json.loads(event["body"])["body"]["payload"]

            try:
                # Check if the data is valid
                DataHandler.validate_data(new_data)

                # Format data
                um = Utility_manager.from_json(new_data)
                formatted_data = um.format_for_first_record()
                # Saving data to db
                resp = db.add(
                    p_key=username,
                    s_key=formatted_data["date"],
                    utilities=formatted_data["utilities"],
                    prices=formatted_data["prices"],
                    cost=formatted_data["cost"],
                )
            except CustomErrorException as ex:
                return response_handler(
                    status_code=STATUS_CODE_BAD_REQUEST,
                    body=json.dumps(ex.to_dict()),
                )

            return response_handler(
                status_code=STATUS_CODE_OK,
                body=json.dumps(
                    {
                        "message": "First record added.",
                    }
                ),
            )


# if __name__ == "__main__":

#     post_event = {
#         "httpMethod": "POST",
#         "requestContext": {
#             "authorizer": {
#                 "claims": {
#                     "cognito:username": "6314f8c2-f0f1-7040-999f-b6a9760702d7",
#                     "email": "test@mail.com",
#                 }
#             }
#         },
#         "body": '{"body":{"payload":{"date":"20250414202539828","utilities":{"gas":20,"electricity":{"t1":20,"t2":30},"water":{"cold":{"kitchen":20,"bathroom":20},"hot":{"kitchen":30,"bathroom":30}}},"prices":{"gas":10,"gas_distribution":5,"electricity":{"t1":10,"t2":20},"water":{"cold":10,"hot":20},"housing":10,"garbage":10,"heat_service":10,"heat_price":10}}}}',
#     }

# get_event = {
#     "httpMethod": "GET",
#     "requestContext": {
#         "authorizer": {
#             "claims": {
#                 "cognito:username": "6314f8c2-f0f1-7040-999f-b6a9760702d7",
#                 "email": "test@mail.com",
#             }
#         }
#     },
# }
# response = lambda_handler(get_event, context={})
# response = lambda_handler(post_event, context={})
