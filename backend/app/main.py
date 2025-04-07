import json

import boto3
from core.models import Utility_manager

STATUS_CODE_OK = 200
ACA_ORIGIN = "*"


class DBHanbler:

    def get_utilities(self) -> list[dict]:
        with open("database.json", "r") as f:
            data = json.load(f)
        return data

    def add_utilities(self, utility):
        with open("database.json", "r") as f:
            data = json.load(f)
            print("Before adding utility:", len(data))
        data.append(utility)
        with open("database.json", "w") as f:
            json.dump(data, f, indent=4)
        print("Utility added to database")
        print("After adding utility:", len(data))


def response_handler(status_code: int, body: dict, origin: str) -> dict:
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": origin,
        },
        "body": json.dumps(body),
    }


def lambda_handler(event: dict, context: dict) -> dict:

    user = (
        event.get("requestContext")
        .get("authorizer")
        .get("claims")
        .get("cognito:username")
    )
    email = event.get("requestContext").get("authorizer").get("claims").get("email")

    db_handler = DBHanbler()

    if event.get("httpMethod") == "GET":

        utilities_list = db_handler.get_utilities()

        return response_handler(
            status_code=STATUS_CODE_OK,
            body={
                "utilities_list": utilities_list,
            },
            origin=ACA_ORIGIN,
        )

    if event.get("httpMethod") == "POST":
        previous_month = db_handler.get_utilities()[-1]
        payload = json.loads(event.get("body")).get("body").get("payload")
        utilities = Utility_manager.from_json(payload)
        result = utilities.calculate_costs(previous_month)

        return response_handler(
            status_code=STATUS_CODE_OK,
            body={
                "result": result,
            },
            origin=ACA_ORIGIN,
        )


# if __name__ == "__main__":

#     body ={
#       "payload":{
#         "date": "2023-08-01",
#         "utilities":{
#             "gas":90,
#             "electricity":{
#                "t1":180,
#                "t2":150
#             },
#             "water":{
#                "cold":{
#                   "kitchen":40,
#                   "bathroom":35,
#                },
#                "hot":{
#                   "kitchen":40,
#                   "bathroom":50
#                }
#             }
#          },
#          "prices":{
#             "gas": 0.5,
#             "gas_distribution": 0.2,
#             "electricity":{
#                "t1":0.4,
#                "t2":0.3
#             },
#             "water":{
#                "cold":0.2,
#                "hot":0.3
#             }
#          }
#       }
#    }

#     event = {
#         "httpMethod": "POST",
#         "requestContext": {
#             "authorizer": {
#                 "claims": {
#                     "cognito:username": "test_user",
#                     "email": "test@mail.com",
#                 }
#             }
#         },
#         "body": json.dumps(body),
#     }
#     context = {}
#     response = lambda_handler(event, context)
