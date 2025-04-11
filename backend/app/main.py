import json
import os

import boto3
from core.db_handler import UtilitiesDB
from core.models import Utility_manager
from core.services import DataHandler, response_handler

STATUS_CODE_OK = 200
ACA_ORIGIN = "*"


# db_arn = "arn:aws:dynamodb:eu-central-1:153061395159:table/utility_manager_db"
db_arn = os.environ["DYNAMO_DB_TABLE"]

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

    # TODO:
    # Add try/except
    # To think about initiation db inside lambda or outside

    if event.get("httpMethod") == "GET":

        resp = db.get_all(user_id=username)

        formatted_data = DataHandler.format_data(resp["Items"])

        return response_handler(
            status_code=STATUS_CODE_OK,
            body={
                "utilities_list": formatted_data,
            },
            origin=ACA_ORIGIN,
        )

    if event.get("httpMethod") == "POST":

        all_data = db.get_all(user_id=username)

        if all_data["Count"] != 0:
            # Get all needed data
            new_data = json.loads(event["body"])["body"]["payload"]
            old_data = all_data["Items"]

            # Format data
            formatted_old_data = DataHandler.format_data(old_data)
            ordered_list = DataHandler.order_by_date(formatted_old_data, "asc")

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

            return response_handler(
                status_code=STATUS_CODE_OK,
                body={
                    "response": all_data["Count"],
                },
                origin=ACA_ORIGIN,
            )
        else:
            # Get new (first) data
            new_data = json.loads(event["body"])["body"]["payload"]

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

            return response_handler(
                status_code=STATUS_CODE_OK,
                body={
                    "message": "First record added.",
                },
                origin=ACA_ORIGIN,
            )


# if __name__ == "__main__":

#     post_event = {
#         "httpMethod": "POST",
#         "requestContext": {
#             "authorizer": {
#                 "claims": {
#                     "cognito:username": "83844892-d021-709c-d9b3-2f30d2f3f24a",
#                     "email": "test@mail.com",
#                 }
#             }
#         },
#         "body": json.dumps(
#             {
#                 "body": {
#                     "payload": {
#                         "date": "20250413253220485",
#                         "utilities": {
#                             "gas": 40,
#                             "electricity": {"t1": 25, "t2": 35},
#                             "water": {
#                                 "cold": {"kitchen": 50, "bathroom": 50},
#                                 "hot": {"kitchen": 50, "bathroom": 40},
#                             },
#                         },
#                         "prices": {
#                             "gas": 15,
#                             "gas_distribution": 10,
#                             "electricity": {"t1": 15, "t2": 25},
#                             "water": {"cold": 15, "hot": 25},
#                         },
#                     }
#                 }
#             }
#         ),
#     }

# get_event = {
#     "httpMethod": "GET",
#     "requestContext": {
#         "authorizer": {
#             "claims": {
#                 "cognito:username": "83844892-d021-709c-d9b3-2f30d2f3f24a",
#                 "email": "test@mail.com",
#             }
#         }
#     },
# "body": json.dumps(),
# }
# response = lambda_handler(get_event, context={})
# response = lambda_handler(post_event, context={})
