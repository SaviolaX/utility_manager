import json

import main
import pytest
from boto3.resources.base import ServiceResource
from core.db_handler import UtilitiesDB
from core.services import DataHandler


@pytest.fixture
def _overrides(dynamodb_table: ServiceResource) -> None:
    main.db = UtilitiesDB(dynamodb_table)


@pytest.fixture
def test_get_event() -> dict:
    return {
        "httpMethod": "GET",
        "requestContext": {
            "authorizer": {
                "claims": {
                    "cognito:username": "test_user",
                    "email": "test@mail.com",
                }
            }
        },
    }


@pytest.fixture
def post_event_body_one() -> dict:
    return {
        "body": {
            "payload": {
                "date": "20250414202539828",
                "utilities": {
                    "gas": 20,
                    "electricity": {"t1": 20, "t2": 30},
                    "water": {
                        "cold": {"kitchen": 20, "bathroom": 20},
                        "hot": {"kitchen": 30, "bathroom": 30},
                    },
                },
                "prices": {
                    "gas": 10,
                    "gas_distribution": 5,
                    "electricity": {"t1": 10, "t2": 20},
                    "water": {"cold": 10, "hot": 20},
                    "housing": 10,
                    "garbage": 10,
                    "heat_service": 10,
                    "heat_price": 10,
                },
            }
        }
    }


@pytest.fixture
def post_event_body_two() -> dict:
    return {
        "body": {
            "payload": {
                "date": "20250514202539828",
                "utilities": {
                    "gas": 30,
                    "electricity": {"t1": 30, "t2": 40},
                    "water": {
                        "cold": {"kitchen": 30, "bathroom": 30},
                        "hot": {"kitchen": 40, "bathroom": 40},
                    },
                },
                "prices": {
                    "gas": 10,
                    "gas_distribution": 5,
                    "electricity": {"t1": 10, "t2": 20},
                    "water": {"cold": 10, "hot": 20},
                    "housing": 10,
                    "garbage": 10,
                    "heat_service": 10,
                    "heat_price": 10,
                },
            }
        }
    }


def post_event(data: dict) -> dict:

    return {
        "httpMethod": "POST",
        "requestContext": {
            "authorizer": {
                "claims": {
                    "cognito:username": "test_user",
                    "email": "test@mail.com",
                }
            }
        },
        "body": json.dumps(data),
    }


@pytest.fixture
def db_record_one() -> dict:
    return {
        "date": "20250414202539828",
        "utilities": {
            "gas": {"current": 30, "previous": 20, "consumption": 10},
            "water": {
                "cold": {
                    "kitchen": {"current": 30, "previous": 20, "consumption": 10},
                    "bathroom": {"current": 30, "previous": 20, "consumption": 10},
                },
                "hot": {
                    "kitchen": {"current": 40, "previous": 30, "consumption": 10},
                    "bathroom": {"current": 40, "previous": 30, "consumption": 10},
                },
            },
            "electricity": {
                "t1": {"current": 30, "previous": 20, "consumption": 10},
                "t2": {"current": 40, "previous": 30, "consumption": 10},
            },
            "heat": {"current": 80, "previous": 60, "consumption": 20},
        },
        "prices": {
            "gas": 10,
            "gas_distribution": 5,
            "electricity": {"t1": 10, "t2": 20},
            "water": {"cold": 10, "hot": 20},
            "heat": 10,
            "heat_service": 10,
            "housing": 10,
            "garbage": 10,
        },
        "cost": {
            "gas": 100,
            "gas_distribution": 5,
            "water": {
                "kitchen_cold": 100,
                "kitchen_hot": 200,
                "bathroom_cold": 100,
                "bathroom_hot": 200,
                "cold": 200,
                "hot": 400,
            },
            "electricity": {"t1": 100, "t2": 200},
            "heat": 200,
            "housing": 10,
            "garbage": 10,
            "total_cost": 1225,
        },
    }


@pytest.fixture
def db_record_two() -> dict:
    return {
        "date": "20250514202539828",  # Next month
        "utilities": {
            "gas": {"current": 40, "previous": 30, "consumption": 10},
            "water": {
                "cold": {
                    "kitchen": {"current": 40, "previous": 30, "consumption": 10},
                    "bathroom": {"current": 40, "previous": 30, "consumption": 10},
                },
                "hot": {
                    "kitchen": {"current": 50, "previous": 40, "consumption": 10},
                    "bathroom": {"current": 50, "previous": 40, "consumption": 10},
                },
            },
            "electricity": {
                "t1": {"current": 40, "previous": 30, "consumption": 10},
                "t2": {"current": 50, "previous": 40, "consumption": 10},
            },
            "heat": {"current": 100, "previous": 80, "consumption": 20},
        },
        "prices": {
            "gas": 10,
            "gas_distribution": 5,
            "electricity": {"t1": 10, "t2": 20},
            "water": {"cold": 10, "hot": 20},
            "heat": 10,
            "heat_service": 10,
            "housing": 10,
            "garbage": 10,
        },
        "cost": {
            "gas": 100,
            "gas_distribution": 5,
            "water": {
                "kitchen_cold": 100,
                "kitchen_hot": 200,
                "bathroom_cold": 100,
                "bathroom_hot": 200,
                "cold": 200,
                "hot": 400,
            },
            "electricity": {"t1": 100, "t2": 200},
            "heat": 200,
            "housing": 10,
            "garbage": 10,
            "total_cost": 1225,
        },
    }


@pytest.mark.usefixtures("_overrides")
def test_get_data__no_items_in_db(test_get_event: dict) -> None:
    resp = main.lambda_handler(test_get_event, None)
    assert resp["statusCode"] == 200
    assert "utilities_list" in resp["body"]
    assert json.loads(resp["body"])["utilities_list"] == []


@pytest.mark.usefixtures("_overrides")
def test_get_data__items_in_db(
    test_get_event: dict, db_record_one: dict, db_record_two: dict
) -> None:
    items = [db_record_one, db_record_two]
    for item in items:
        main.db.add(
            p_key="test_user",
            s_key=item["date"],
            utilities=item["utilities"],
            prices=item["prices"],
            cost=item["cost"],
        )
    resp = main.lambda_handler(test_get_event, None)
    resp_body = json.loads(resp["body"])

    assert resp["statusCode"] == 200
    assert "utilities_list" in resp_body
    assert len(resp_body["utilities_list"]) == 2

    # DynamoDB returns items in ascending order by default
    assert resp_body["utilities_list"][0]["date"] == db_record_one["date"]
    assert resp_body["utilities_list"][1]["date"] == db_record_two["date"]

    assert resp_body["utilities_list"][0]["formattedDate"] == DataHandler.format_date(
        db_record_one["date"]
    )
    assert resp_body["utilities_list"][1]["formattedDate"] == DataHandler.format_date(
        db_record_two["date"]
    )


def test_get_data___error(test_get_event: dict) -> None:
    # Simulate a database error
    main.db = UtilitiesDB("")
    resp = main.lambda_handler(test_get_event, None)
    resp_body = json.loads(resp["body"])
    assert resp["statusCode"] == 400
    assert resp_body["error"] == "AttributeError"


@pytest.mark.usefixtures("_overrides")
def test_post_data__initial_record(
    db_record_one: dict, post_event_body_one: dict
) -> None:
    resp = main.lambda_handler(post_event(post_event_body_one), None)
    resp_body = json.loads(resp["body"])

    assert resp["statusCode"] == 200
    assert resp_body["message"] == "First record added."

    # Check if the record was added to the database
    response = main.db.get_all("test_user")
    assert response["Count"] == 1
    assert response["Items"][0]["UserId"] == "test_user"
    assert response["Items"][0]["Date"] == db_record_one["date"]


@pytest.mark.usefixtures("_overrides")
def test_post_data__initial_record_date_value_error() -> None:
    data = {
        "body": {
            "payload": {
                "date": "",  # Error should be here
                "utilities": {
                    "gas": 20,
                    "electricity": {"t1": 20, "t2": 30},
                    "water": {
                        "cold": {"kitchen": 20, "bathroom": 20},
                        "hot": {"kitchen": 30, "bathroom": 30},
                    },
                },
                "prices": {
                    "gas": 10,
                    "gas_distribution": 5,
                    "electricity": {"t1": 10, "t2": 20},
                    "water": {"cold": 10, "hot": 20},
                    "housing": 10,
                    "garbage": 10,
                    "heat_service": 10,
                    "heat_price": 10,
                },
            }
        }
    }
    resp = main.lambda_handler(post_event(data), None)
    resp_body = json.loads(resp["body"])
    assert resp["statusCode"] == 400
    assert resp_body["error"] == "ValueError"
    assert resp_body["message"] == "Missing value for date"


@pytest.mark.usefixtures("_overrides")
def test_post_data__initial_record_t1_value_error() -> None:
    data = {
        "body": {
            "payload": {
                "date": "20250414202539828",
                "utilities": {
                    "gas": 20,
                    "electricity": {"t1": None, "t2": 30},  # Error should be here
                    "water": {
                        "cold": {"kitchen": 20, "bathroom": 20},
                        "hot": {"kitchen": 30, "bathroom": 30},
                    },
                },
                "prices": {
                    "gas": 10,
                    "gas_distribution": 5,
                    "electricity": {"t1": 10, "t2": 20},
                    "water": {"cold": 10, "hot": 20},
                    "housing": 10,
                    "garbage": 10,
                    "heat_service": 10,
                    "heat_price": 10,
                },
            }
        }
    }
    resp = main.lambda_handler(post_event(data), None)
    resp_body = json.loads(resp["body"])
    assert resp["statusCode"] == 400
    assert resp_body["error"] == "ValueError"
    assert resp_body["message"] == "Missing value for t1"


@pytest.mark.usefixtures("_overrides")
def test_post_data__second_record(
    db_record_one: dict, db_record_two: dict, post_event_body_two: dict
) -> None:
    # First record
    main.db.add(
        p_key="test_user",
        s_key=db_record_one["date"],
        utilities=db_record_one["utilities"],
        prices=db_record_one["prices"],
        cost=db_record_one["cost"],
    )

    resp = main.lambda_handler(post_event(post_event_body_two), None)
    resp_body = json.loads(resp["body"])

    assert resp["statusCode"] == 200
    assert resp_body["message"] == "New record created."

    # Check if the second record was added to the database
    # DynamoDB returns items in ascending order by default
    response = main.db.get_all("test_user")
    assert response["Count"] == 2
    assert response["Items"][1]["UserId"] == "test_user"
    assert response["Items"][1]["Date"] == db_record_two["date"]


@pytest.mark.usefixtures("_overrides")
def test_post_data__second_record_date_value_error(db_record_one: dict) -> None:
    data = {
        "body": {
            "payload": {
                "date": "",  # Error should be here
                "utilities": {
                    "gas": 20,
                    "electricity": {"t1": 20, "t2": 30},
                    "water": {
                        "cold": {"kitchen": 20, "bathroom": 20},
                        "hot": {"kitchen": 30, "bathroom": 30},
                    },
                },
                "prices": {
                    "gas": 10,
                    "gas_distribution": 5,
                    "electricity": {"t1": 10, "t2": 20},
                    "water": {"cold": 10, "hot": 20},
                    "housing": 10,
                    "garbage": 10,
                    "heat_service": 10,
                    "heat_price": 10,
                },
            }
        }
    }

    # First record
    main.db.add(
        p_key="test_user",
        s_key=db_record_one["date"],
        utilities=db_record_one["utilities"],
        prices=db_record_one["prices"],
        cost=db_record_one["cost"],
    )
    response = main.db.get_all("test_user")
    assert response["Count"] == 1

    resp = main.lambda_handler(post_event(data), None)
    resp_body = json.loads(resp["body"])
    assert resp["statusCode"] == 400
    assert resp_body["error"] == "ValueError"
    assert resp_body["message"] == "Missing value for date"


@pytest.mark.usefixtures("_overrides")
def test_post_data__second_record_t1_value_error(db_record_one: dict) -> None:
    data = {
        "body": {
            "payload": {
                "date": "20250414202539828",
                "utilities": {
                    "gas": 20,
                    "electricity": {"t1": None, "t2": 30},  # Error should be here
                    "water": {
                        "cold": {"kitchen": 20, "bathroom": 20},
                        "hot": {"kitchen": 30, "bathroom": 30},
                    },
                },
                "prices": {
                    "gas": 10,
                    "gas_distribution": 5,
                    "electricity": {"t1": 10, "t2": 20},
                    "water": {"cold": 10, "hot": 20},
                    "housing": 10,
                    "garbage": 10,
                    "heat_service": 10,
                    "heat_price": 10,
                },
            }
        }
    }

    # First record
    main.db.add(
        p_key="test_user",
        s_key=db_record_one["date"],
        utilities=db_record_one["utilities"],
        prices=db_record_one["prices"],
        cost=db_record_one["cost"],
    )
    response = main.db.get_all("test_user")
    assert response["Count"] == 1

    resp = main.lambda_handler(post_event(data), None)
    resp_body = json.loads(resp["body"])
    assert resp["statusCode"] == 400
    assert resp_body["error"] == "ValueError"
    assert resp_body["message"] == "Missing value for t1"
