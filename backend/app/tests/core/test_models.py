import pytest
from core.models import Utility_manager


@pytest.fixture
def test_first_input_values() -> dict:
    return {
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


@pytest.fixture
def test_second_input_values() -> dict:
    return {
        "date": "20250414202539828",
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


@pytest.fixture
def test_database_normal_record() -> dict:
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
def test_format_for_first_record_response() -> dict:
    return {
        "date": "20250414202539828",
        "utilities": {
            "gas": {
                "current": 20,
                "previous": "?",
                "consumption": "?",
            },
            "water": {
                "cold": {
                    "kitchen": {
                        "current": 20,
                        "previous": "?",
                        "consumption": "?",
                    },
                    "bathroom": {
                        "current": 20,
                        "previous": "?",
                        "consumption": "?",
                    },
                },
                "hot": {
                    "kitchen": {
                        "current": 30,
                        "previous": "?",
                        "consumption": "?",
                    },
                    "bathroom": {
                        "current": 30,
                        "previous": "?",
                        "consumption": "?",
                    },
                },
            },
            "electricity": {
                "t1": {
                    "current": 20,
                    "previous": "?",
                    "consumption": "?",
                },
                "t2": {
                    "current": 30,
                    "previous": "?",
                    "consumption": "?",
                },
            },
            "heat": {
                "current": 60,
                "previous": "?",
                "consumption": "?",
            },
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
            "gas": "?",
            "water": {
                "kitchen_cold": "?",
                "kitchen_hot": "?",
                "bathroom_cold": "?",
                "bathroom_hot": "?",
                "cold": "?",
                "hot": "?",
            },
            "electricity": {"t1": "?", "t2": "?", "total": "?"},
            "heat": 10,
            "housing": 10,
            "garbage": 10,
            "total_cost": "?",
        },
    }


def test_utility_manager_from_json(test_first_input_values: dict) -> None:
    um = Utility_manager.from_json(test_first_input_values)

    assert um.date == test_first_input_values["date"]
    # Consumption
    assert um.gas.consumption == test_first_input_values["utilities"]["gas"]
    assert (
        um.electricity.t1_consumption
        == test_first_input_values["utilities"]["electricity"]["t1"]
    )
    assert (
        um.electricity.t2_consumption
        == test_first_input_values["utilities"]["electricity"]["t2"]
    )
    assert (
        um.water.cold_bathroom_consumption
        == test_first_input_values["utilities"]["water"]["cold"]["bathroom"]
    )
    assert (
        um.water.cold_kitchen_consumption
        == test_first_input_values["utilities"]["water"]["cold"]["kitchen"]
    )
    assert (
        um.water.hot_bathroom_consumption
        == test_first_input_values["utilities"]["water"]["hot"]["bathroom"]
    )
    assert (
        um.water.hot_kitchen_consumption
        == test_first_input_values["utilities"]["water"]["hot"]["kitchen"]
    )

    # Prices
    assert um.price.gas == test_first_input_values["prices"]["gas"]
    assert (
        um.price.gas_distribution
        == test_first_input_values["prices"]["gas_distribution"]
    )
    assert um.price.t1 == test_first_input_values["prices"]["electricity"]["t1"]
    assert um.price.t2 == test_first_input_values["prices"]["electricity"]["t2"]
    assert um.price.cold == test_first_input_values["prices"]["water"]["cold"]
    assert um.price.hot == test_first_input_values["prices"]["water"]["hot"]
    assert um.price.housing == test_first_input_values["prices"]["housing"]
    assert um.price.garbage == test_first_input_values["prices"]["garbage"]
    assert um.price.heat_service == test_first_input_values["prices"]["heat_service"]
    assert um.price.heat_price == test_first_input_values["prices"]["heat_price"]


def test_utility_manager_format_for_first_record(
    test_first_input_values: dict,
    test_format_for_first_record_response: dict,
) -> None:
    um = Utility_manager.from_json(test_first_input_values)
    formatted_data = um.format_for_first_record()

    assert formatted_data == test_format_for_first_record_response


def test_utility_manager_calculate_costs(
    test_second_input_values: dict,
    test_format_for_first_record_response: dict,
    test_database_normal_record: dict,
) -> None:
    um = Utility_manager.from_json(test_second_input_values)
    formatted_data = um.calculate_costs(test_format_for_first_record_response)

    assert formatted_data == test_database_normal_record


def test_utility_manager__calculate_heat(
    test_second_input_values: dict, test_format_for_first_record_response: dict
) -> None:
    um = Utility_manager.from_json(test_second_input_values)
    result = um._calculate_heat(
        test_format_for_first_record_response["utilities"]["heat"],
    )

    assert (
        result["current"]
        == um.water.hot_kitchen_consumption + um.water.hot_bathroom_consumption
    )
    assert (
        result["previous"]
        == test_format_for_first_record_response["utilities"]["heat"]["current"]
    )
    assert result["consumption"] == result["current"] - result["previous"]
    assert result["cost"] == result["consumption"] * um.price.heat_price


def test_utility_manager__calculate_gas(
    test_second_input_values: dict, test_format_for_first_record_response: dict
) -> None:
    um = Utility_manager.from_json(test_second_input_values)
    result = um._calculate_gas(
        test_format_for_first_record_response["utilities"]["gas"],
    )

    assert result["current"] == um.gas.consumption
    assert (
        result["previous"]
        == test_format_for_first_record_response["utilities"]["gas"]["current"]
    )
    assert result["consumption"] == result["current"] - result["previous"]
    assert result["cost"] == result["consumption"] * um.price.gas


def test_utility_manager__calculate_electricity(
    test_second_input_values: dict, test_format_for_first_record_response: dict
) -> None:
    um = Utility_manager.from_json(test_second_input_values)
    result = um._calculate_electricity(
        test_format_for_first_record_response["utilities"]["electricity"],
    )

    assert result["t1"]["current"] == um.electricity.t1_consumption
    assert (
        result["t1"]["previous"]
        == test_format_for_first_record_response["utilities"]["electricity"]["t1"][
            "current"
        ]
    )
    assert result["t2"]["current"] == um.electricity.t2_consumption
    assert (
        result["t2"]["previous"]
        == test_format_for_first_record_response["utilities"]["electricity"]["t2"][
            "current"
        ]
    )
    assert (
        result["t1"]["consumption"]
        == result["t1"]["current"] - result["t1"]["previous"]
    )
    assert (
        result["t2"]["consumption"]
        == result["t2"]["current"] - result["t2"]["previous"]
    )


def test_utility_manager__calculate_water(
    test_second_input_values: dict, test_format_for_first_record_response: dict
) -> None:
    um = Utility_manager.from_json(test_second_input_values)
    result = um._calculate_water(
        test_format_for_first_record_response["utilities"]["water"],
    )

    assert result["cold"]["kitchen"]["current"] == um.water.cold_kitchen_consumption
    assert (
        result["cold"]["kitchen"]["previous"]
        == test_format_for_first_record_response["utilities"]["water"]["cold"][
            "kitchen"
        ]["current"]
    )
    assert result["cold"]["bathroom"]["current"] == um.water.cold_bathroom_consumption
    assert (
        result["cold"]["bathroom"]["previous"]
        == test_format_for_first_record_response["utilities"]["water"]["cold"][
            "bathroom"
        ]["current"]
    )

    assert result["cold"]["total_consumption"] == (
        (
            um.water.cold_kitchen_consumption
            - test_format_for_first_record_response["utilities"]["water"]["cold"][
                "kitchen"
            ]["current"]
        )
        + (
            um.water.cold_bathroom_consumption
            - test_format_for_first_record_response["utilities"]["water"]["cold"][
                "bathroom"
            ]["current"]
        )
    )
    assert result["hot"]["kitchen"]["current"] == um.water.hot_kitchen_consumption
    assert (
        result["hot"]["kitchen"]["previous"]
        == test_format_for_first_record_response["utilities"]["water"]["hot"][
            "kitchen"
        ]["current"]
    )
    assert result["hot"]["bathroom"]["current"] == um.water.hot_bathroom_consumption
    assert (
        result["hot"]["bathroom"]["previous"]
        == test_format_for_first_record_response["utilities"]["water"]["hot"][
            "bathroom"
        ]["current"]
    )
    assert result["hot"]["total_consumption"] == (
        (
            um.water.hot_kitchen_consumption
            - test_format_for_first_record_response["utilities"]["water"]["hot"][
                "kitchen"
            ]["current"]
        )
        + (
            um.water.hot_bathroom_consumption
            - test_format_for_first_record_response["utilities"]["water"]["hot"][
                "bathroom"
            ]["current"]
        )
    )
    assert (
        result["cost"]["kitchen_cold"]
        == result["cold"]["kitchen"]["consumption"] * um.price.cold
    )
    assert (
        result["cost"]["kitchen_hot"]
        == result["hot"]["kitchen"]["consumption"] * um.price.hot
    )
    assert (
        result["cost"]["bathroom_cold"]
        == result["cold"]["bathroom"]["consumption"] * um.price.cold
    )
    assert (
        result["cost"]["bathroom_hot"]
        == result["hot"]["bathroom"]["consumption"] * um.price.hot
    )

    assert result["cost"]["cold"] == result["cold"]["total_consumption"] * um.price.cold
    assert result["cost"]["hot"] == result["hot"]["total_consumption"] * um.price.hot
    assert result["cost"]["total_cost"] == (
        result["cost"]["kitchen_cold"]
        + result["cost"]["kitchen_hot"]
        + result["cost"]["bathroom_cold"]
        + result["cost"]["bathroom_hot"]
    )
