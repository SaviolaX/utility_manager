import json

import boto3
from core.db_handler import UtilitiesDB
from core.models import Utility_manager
from core.services import response_handler

STATUS_CODE_OK = 200
ACA_ORIGIN = "*"


db_arn = "arn:aws:dynamodb:eu-central-1:153061395159:table/utility_manager_db"

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
    # Convert date from single line in frontend
    # Fix watch method after first item loaded
    # Update items after post request
    # Add try/except
    # To think about initiation db inside lambda or outside

    if event.get("httpMethod") == "GET":
        with open("database.json", "r") as f:
            data = json.load(f)

        resp = db.get_all(user_id=username)
        print(resp)

        return response_handler(
            status_code=STATUS_CODE_OK,
            body={
                "utilities_list": resp["Items"],
            },
            origin=ACA_ORIGIN,
        )

    if event.get("httpMethod") == "POST":

        all_data = db.get_all(user_id=username)

        if all_data["Count"] != 0:
            # new_data = json.loads(event["body"])["body"]["payload"]
            # old_data = data[-1]

            # um = Utility_manager.from_json(new_data)
            # result = um.calculate_costs(old_data)

            # resp = db.add(
            #     p_key=username,
            #     s_key=result["date"],
            #     utilities=result["utilities"],
            #     prices=result["prices"],
            #     cost=result["cost"],
            # )

            return response_handler(
                status_code=STATUS_CODE_OK,
                body={
                    "response": all_data["Count"],
                },
                origin=ACA_ORIGIN,
            )
        else:
            new_data = json.loads(event["body"])["body"]["payload"]
            um = Utility_manager.from_json(new_data)
            formatted_data = um.format_for_first_record()
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
#                     "cognito:username": "test_user",
#                     "email": "test@mail.com",
#                 }
#             }
#         },
#         "body": '{"body":{"payload":{"utilities":{"gas":123,"electricity":{"t1":222,"t2":222},"water":{"cold":{"kitchen":123,"bathroom":123},"hot":{"kitchen":123,"bathroom":123}}},"prices":{"gas":0.5,"gas_distribution":0.1,"electricity":{"t1":0.4,"t2":0.3},"water":{"cold":0.2,"hot":0.3}}}}}',
#     }

#     get_event = {
#         "httpMethod": "GET",
#         "requestContext": {
#             "authorizer": {
#                 "claims": {
#                     "cognito:username": "test_user",
#                     "email": "test@mail.com",
#                 }
#             }
#         },
#         # "body": json.dumps(),
#     }
#     context = {}
#     # response = lambda_handler(get_event, context)
#     response = lambda_handler(post_event, context)
