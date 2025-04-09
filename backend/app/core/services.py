import json


def response_handler(status_code: int, body: dict, origin: str) -> dict:
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": origin,
        },
        "body": json.dumps(body),
    }
