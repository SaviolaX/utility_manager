import json
from typing import Any


class DataHandler:

    @classmethod
    def format_date(cls, date: str) -> str:
        year = date[0:4]
        month = date[4:6]
        day = date[6:8]

        full_date = f"{year}.{month}.{day}"
        return full_date

    @classmethod
    def format_data(cls, data: list[dict]) -> list[dict]:
        """
        Format the data from the DynamoDB to needed format
        for the frontend and for calculations.
        """
        new_data = []
        for item in data:
            new_data.append(
                {
                    "date": item.get("Date"),
                    "formattedDate": cls.format_date(item.get("Date")),
                    "userId": item.get("UserId"),
                    "utilities": json.loads(item.get("Utilities")),
                    "prices": json.loads(item.get("Prices")),
                    "cost": json.loads(item.get("Cost")),
                }
            )
        return new_data

    @classmethod
    def order_by_date(cls, data: list[dict], order: str = "asc") -> list[dict]:
        if order == "asc":
            return sorted(data, key=lambda d: d["formattedDate"])
        else:  # desc
            return sorted(data, key=lambda d: d["formattedDate"], reverse=True)

    @classmethod
    def validate_data(cls, data: dict) -> bool:
        """
        Validate the data from the frontend.
        """
        try:
            for key, value in data.items():
                if value is None:
                    raise ValueError(f"Missing value for {key}")
                elif type(value) is str:
                    if not value.strip():
                        raise ValueError(f"Missing value for {key}")
                elif isinstance(value, dict):
                    cls.validate_data(value)
            return data
        except ValueError as ex:
            raise CustomErrorException(type(ex).__name__, str(ex)) from ex


def response_handler(
    status_code: int,
    body: str,
    content_type: str = "application/json",
    ac_allow_origin: str = "*",
    ac_allow_headers: str = "*",
) -> dict[str, Any]:
    response = {
        "statusCode": status_code,
        "headers": {
            "Content-Type": content_type,
            "Access-Control-Allow-Origin": ac_allow_origin,
            "Access-Control-Allow-Headers": ac_allow_headers,
        },
        "body": body,
    }
    return response


class CustomErrorException(Exception):
    def __init__(self, error: str, message: str):
        self.error = error
        self.message = message
        super().__init__(f"{error}: {message}")

    def to_dict(self):
        return {"error": self.error, "message": self.message}
