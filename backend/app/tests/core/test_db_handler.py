import json

import pytest
from boto3.resources.base import ServiceResource
from core.db_handler import UtilitiesDB
from core.services import CustomErrorException


def test_add_item(dynamodb_table: ServiceResource) -> None:
    item = {
        "userId": "test_user",
        "date": "20250414202539828",
        "utilities": {"electricity": 100, "water": 50},
        "prices": {"electricity": 0.2, "water": 0.1},
        "cost": {"electricity": 20, "water": 5},
    }
    db = UtilitiesDB(dynamodb_table)
    db.add(
        p_key=item["userId"],
        s_key=item["date"],
        utilities=item["utilities"],
        prices=item["prices"],
        cost=item["cost"],
    )
    response = dynamodb_table.get_item(
        Key={"UserId": item["userId"], "Date": item["date"]}
    )
    assert "Item" in response
    assert response["Item"]["UserId"] == item["userId"]
    assert response["Item"]["Date"] == item["date"]
    assert response["Item"]["Utilities"] == json.dumps(item["utilities"])
    assert response["Item"]["Prices"] == json.dumps(item["prices"])
    assert response["Item"]["Cost"] == json.dumps(item["cost"])


def test_add_item_error() -> None:
    dynamodb_table = None
    db = UtilitiesDB(dynamodb_table)
    with pytest.raises(CustomErrorException) as ex:
        db.add(
            p_key="test_user",
            s_key="20250414202539828",
            utilities={"electricity": 100, "water": 50},
            prices={"electricity": 0.2, "water": 0.1},
            cost={"electricity": 20, "water": 5},
        )
    assert ex.value.error == "AttributeError"
    assert ex.value.message == "'NoneType' object has no attribute 'put_item'"


def test_get_all(dynamodb_table: ServiceResource) -> None:
    items = [
        {
            "UserId": "test_user",
            "Date": "20250414202539828",
            "Utilities": json.dumps({"electricity": 100, "water": 50}),
            "Prices": json.dumps({"electricity": 0.2, "water": 0.1}),
            "Cost": json.dumps({"electricity": 20, "water": 5}),
        },
        {
            "UserId": "test_user",
            "Date": "20250314202539828",
            "Utilities": json.dumps({"electricity": 150, "water": 60}),
            "Prices": json.dumps({"electricity": 0.25, "water": 0.15}),
            "Cost": json.dumps({"electricity": 37.5, "water": 9}),
        },
    ]

    for item in items:
        dynamodb_table.put_item(Item=item)

    db = UtilitiesDB(dynamodb_table)
    response = db.get_all("test_user")
    assert response["Count"] == len(items)
    for item in response["Items"]:
        assert any(
            i["UserId"] == item["UserId"] and i["Date"] == item["Date"]
            for i in response["Items"]
        )


def test_get_all_error() -> None:
    dynamodb_table = None
    db = UtilitiesDB(dynamodb_table)
    with pytest.raises(CustomErrorException) as ex:
        db.get_all("test_user")
    assert ex.value.error == "AttributeError"
    assert ex.value.message == "'NoneType' object has no attribute 'scan'"
