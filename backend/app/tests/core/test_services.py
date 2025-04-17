import pytest
from core.services import CustomErrorException, DataHandler, response_handler


@pytest.fixture
def test_data_from_db() -> None:
    return [
        {
            "UserId": "test_user",
            "Date": "20250414202539828",
            "Utilities": '{"electricity": 100, "water": 50}',
            "Prices": '{"electricity": 0.2, "water": 0.1}',
            "Cost": '{"electricity": 20, "water": 5}',
        },
        {
            "UserId": "test_user",
            "Date": "20250314202539828",
            "Utilities": '{"electricity": 150, "water": 60}',
            "Prices": '{"electricity": 0.25, "water": 0.15}',
            "Cost": '{"electricity": 37.5, "water": 9}',
        },
    ]


def test_format_date() -> None:
    assert DataHandler.format_date("20250414202539828") == "2025.04.14"
    assert DataHandler.format_date("20250314202539828") == "2025.03.14"
    assert DataHandler.format_date("20250412202539828") == "2025.04.12"


def test_format_data(test_data_from_db: list[dict]) -> None:
    formatted_data = DataHandler.format_data(test_data_from_db)
    assert len(formatted_data) == 2

    assert formatted_data[0]["date"] == "20250414202539828"
    assert formatted_data[0]["formattedDate"] == "2025.04.14"
    assert formatted_data[0]["userId"] == "test_user"
    assert formatted_data[0]["utilities"] == {"electricity": 100, "water": 50}
    assert formatted_data[0]["prices"] == {"electricity": 0.2, "water": 0.1}
    assert formatted_data[0]["cost"] == {"electricity": 20, "water": 5}

    assert formatted_data[1]["date"] == "20250314202539828"
    assert formatted_data[1]["formattedDate"] == "2025.03.14"
    assert formatted_data[1]["userId"] == "test_user"
    assert formatted_data[1]["utilities"] == {"electricity": 150, "water": 60}
    assert formatted_data[1]["prices"] == {"electricity": 0.25, "water": 0.15}
    assert formatted_data[1]["cost"] == {"electricity": 37.5, "water": 9}


def test_order_by_date(test_data_from_db: list[dict]) -> None:
    formatted_data = DataHandler.format_data(test_data_from_db)
    ordered_data_asc = DataHandler.order_by_date(formatted_data, "asc")
    ordered_data_desc = DataHandler.order_by_date(formatted_data, "desc")

    assert ordered_data_asc[0]["date"] == "20250314202539828"
    assert ordered_data_asc[1]["date"] == "20250414202539828"

    assert ordered_data_desc[0]["date"] == "20250414202539828"
    assert ordered_data_desc[1]["date"] == "20250314202539828"


def test_validate_data__correct() -> None:
    data = {
        "date": "20250414202539828",
        "utilities": {
            "gas": 10,
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
    assert DataHandler.validate_data(data) == data


def test_validate_data__no_gas_value() -> None:
    data = {
        "date": "20250414202539828",
        "utilities": {
            "gas": None,  # This should raise an error
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
    with pytest.raises(CustomErrorException) as ex:
        DataHandler.validate_data(data)
    assert str(ex.value) == "ValueError: Missing value for gas"


def test_validate_data__no_t1_value() -> None:
    data = {
        "date": "20250414202539828",
        "utilities": {
            "gas": 10,
            "electricity": {"t1": None, "t2": 30}, # t1 should raise an error
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
    with pytest.raises(CustomErrorException) as ex:
        DataHandler.validate_data(data)
    assert str(ex.value) == "ValueError: Missing value for t1"

def test_validate_data__no_date_value() -> None:
    data = {
        "date": "",
        "utilities": {
            "gas": 10,
            "electricity": {"t1": 20, "t2": 30}, # t1 should raise an error
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
    with pytest.raises(CustomErrorException) as ex:
        DataHandler.validate_data(data)
    assert str(ex.value) == "ValueError: Missing value for date"



def test_response_handler() -> None:
    response = response_handler(
        status_code=200,
        body='{"message": "success"}',
        content_type="application/json",
        ac_allow_origin="*",
        ac_allow_headers="*",
    )
    assert response["statusCode"] == 200
    assert response["headers"]["Content-Type"] == "application/json"
    assert response["headers"]["Access-Control-Allow-Origin"] == "*"
    assert response["headers"]["Access-Control-Allow-Headers"] == "*"
    assert response["body"] == '{"message": "success"}'


def test_custom_error_exception() -> None:
    error = CustomErrorException("CustomError", "This is a custom error")
    assert error.error == "CustomError"
    assert error.message == "This is a custom error"
    assert error.to_dict() == {
        "error": "CustomError",
        "message": "This is a custom error",
    }


def test_custom_error_exception_zero_division_error() -> None:
    try:
        2 / 0
    except Exception as ex:
        error = CustomErrorException(type(ex).__name__, str(ex))
        assert error.error == "ZeroDivisionError"
        assert error.message == "division by zero"
        assert error.to_dict() == {
            "error": "ZeroDivisionError",
            "message": "division by zero",
        }
