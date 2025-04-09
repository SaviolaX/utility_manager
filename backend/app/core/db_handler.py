import json
from dataclasses import dataclass

from boto3.dynamodb.conditions import Attr
from boto3.resources.base import ServiceResource


@dataclass
class UtilitiesDB:
    db_table: ServiceResource

    def add(
        self, p_key: str, s_key: str, utilities: dict, prices: dict, cost: dict
    ) -> dict:
        return self.db_table.put_item(
            Item={
                "UserId": p_key,
                "Date": s_key,
                "Utilities": json.dumps(utilities),
                "Prices": json.dumps(prices),
                "Cost": json.dumps(cost),
            }
        )

    def get_all(self, user_id: str) -> list[dict]:
        return self.db_table.scan(FilterExpression=Attr("UserId").eq(user_id))
