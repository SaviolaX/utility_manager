import json


class DataHandler:

    @classmethod
    def format_date(cls, date: str) -> str:
        year = date[0:4]
        month = date[4:6]
        day = date[6:8]

        full_date = f"{year}.{month}.{day}"
        return full_date

    @classmethod
    def format_data(cls, data: dict[str]) -> list[dict]:
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


def response_handler(status_code: int, body: dict, origin: str) -> dict:
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": origin,
        },
        "body": json.dumps(body),
    }
