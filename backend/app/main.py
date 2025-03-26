import json
from core.models import Printer


def lambda_handler(event: dict, context: dict) -> dict:

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "event": event,
                "message": "Lambda hendler message!"
            }
        ),
    }
