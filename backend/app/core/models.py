from dataclasses import dataclass


@dataclass
class Water:
    cold_kitchen_consumption: float
    hot_kitchen_consumption: float
    cold_bathroom_consumption: float
    hot_bathroom_consumption: float


@dataclass
class Electricity:
    t1_consumption: float
    t2_consumption: float


@dataclass
class Gas:
    consumption: float


@dataclass
class Price:
    gas: float
    gas_distribution: float
    t1: float
    t2: float
    cold: float
    hot: float


@dataclass
class Utility_manager:
    gas: Gas
    electricity: Electricity
    water: Water
    price: Price
    date: str

    @classmethod
    def from_json(cls, data: dict) -> "Utility_manager":
        """
        Fill the dataclass with data from the json file.
        """
        return cls(
            date=data["date"],
            gas=Gas(consumption=data["utilities"]["gas"]),
            electricity=Electricity(
                t1_consumption=data["utilities"]["electricity"]["t1"],
                t2_consumption=data["utilities"]["electricity"]["t2"],
            ),
            water=Water(
                cold_kitchen_consumption=data["utilities"]["water"]["cold"]["kitchen"],
                hot_kitchen_consumption=data["utilities"]["water"]["hot"]["kitchen"],
                cold_bathroom_consumption=data["utilities"]["water"]["cold"][
                    "bathroom"
                ],
                hot_bathroom_consumption=data["utilities"]["water"]["hot"]["bathroom"],
            ),
            price=Price(
                gas=data["prices"]["gas"],
                gas_distribution=data["prices"]["gas_distribution"],
                t1=data["prices"]["electricity"]["t1"],
                t2=data["prices"]["electricity"]["t2"],
                cold=data["prices"]["water"]["cold"],
                hot=data["prices"]["water"]["hot"],
            ),
        )

    def calculate_costs(self, previous_inputs: dict) -> dict:
        gas_results = self._calculate_gas(previous_inputs["utilities"]["gas"])
        water_results = self._calculate_water(previous_inputs["utilities"]["water"])
        electricity_results = self._calculate_electricity(
            previous_inputs["utilities"]["electricity"]
        )
        total_cost = (
            gas_results["total_cost"]
            + water_results["cost"]["total_cost"]
            + electricity_results["cost"]["total_cost"]
        )
        return {
            "date": self.date,
            "utilities": {
                "gas": {
                    "current": gas_results["current"],
                    "previous": gas_results["previous"],
                    "consumption": gas_results["consumption"],
                },
                "water": {
                    "cold": {
                        "kitchen": {
                            "current": water_results["cold"]["kitchen"]["current"],
                            "previous": water_results["cold"]["kitchen"]["previous"],
                            "consumption": water_results["cold"]["kitchen"][
                                "consumption"
                            ],
                        },
                        "bathroom": {
                            "current": water_results["cold"]["bathroom"]["current"],
                            "previous": water_results["cold"]["bathroom"]["previous"],
                            "consumption": water_results["cold"]["bathroom"][
                                "consumption"
                            ],
                        },
                    },
                    "hot": {
                        "kitchen": {
                            "current": water_results["hot"]["kitchen"]["current"],
                            "previous": water_results["hot"]["kitchen"]["previous"],
                            "consumption": water_results["hot"]["kitchen"][
                                "consumption"
                            ],
                        },
                        "bathroom": {
                            "current": water_results["hot"]["bathroom"]["current"],
                            "previous": water_results["hot"]["bathroom"]["previous"],
                            "consumption": water_results["hot"]["bathroom"][
                                "consumption"
                            ],
                        },
                    },
                },
                "electricity": {
                    "t1": {
                        "current": electricity_results["t1"]["current"],
                        "previous": electricity_results["t1"]["previous"],
                        "consumption": electricity_results["t1"]["consumption"],
                    },
                    "t2": {
                        "current": electricity_results["t2"]["current"],
                        "previous": electricity_results["t2"]["previous"],
                        "consumption": electricity_results["t2"]["consumption"],
                    },
                },
            },
            "prices": {
                "gas": self.price.gas,
                "gas_distribution": self.price.gas_distribution,
                "electricity": {"t1": self.price.t1, "t2": self.price.t2},
                "water": {"cold": self.price.cold, "hot": self.price.hot},
            },
            "cost": {
                "gas": gas_results["cost"],
                "water": {
                    "kitchen_cold": water_results["cost"]["kitchen_cold"],
                    "kitchen_hot": water_results["cost"]["kitchen_hot"],
                    "bathroom_cold": water_results["cost"]["bathroom_cold"],
                    "bathroom_hot": water_results["cost"]["bathroom_hot"],
                    "cold": water_results["cost"]["cold"],
                    "hot": water_results["cost"]["hot"],
                },
                "electricity": {
                    "t1": electricity_results["cost"]["t1"],
                    "t2": electricity_results["cost"]["t2"],
                },
                "total_cost": total_cost,
            },
        }

    def _calculate_gas(self, previous_gas: dict) -> dict:
        """
        Calculate the gas consumption and costs.
        """
        gas_consumption = self.gas.consumption - previous_gas["current"]
        gas_cost = gas_consumption * self.price.gas
        total_cost = gas_cost + self.price.gas_distribution
        return {
            "current": self.gas.consumption,
            "previous": previous_gas["current"],
            "consumption": gas_consumption,
            "cost": gas_cost,
            "total_cost": total_cost,
        }

    def _calculate_electricity(self, previous_electricity: dict) -> dict:
        """
        Calculate the electricity consumption and costs.
        """
        t1_consumption = (
            self.electricity.t1_consumption - previous_electricity["t1"]["current"]
        )
        t2_consumption = (
            self.electricity.t2_consumption - previous_electricity["t2"]["current"]
        )
        t1_cost = t1_consumption * self.price.t1
        t2_cost = t2_consumption * self.price.t2
        total_cost = t1_cost + t2_cost
        return {
            "t1": {
                "current": self.electricity.t1_consumption,
                "previous": previous_electricity["t1"]["current"],
                "consumption": t1_consumption,
                "cost": t1_cost,
            },
            "t2": {
                "current": self.electricity.t2_consumption,
                "previous": previous_electricity["t2"]["current"],
                "consumption": t2_consumption,
                "cost": t2_cost,
            },
            "cost": {"t1": t1_cost, "t2": t2_cost, "total_cost": total_cost},
        }

    def _calculate_water(self, previous_water: dict) -> dict:
        """
        Calculate the water consumption and costs.
        """
        cold_kitchen_consumption = (
            self.water.cold_kitchen_consumption
            - previous_water["cold"]["kitchen"]["current"]
        )
        hot_kitchen_consumption = (
            self.water.hot_kitchen_consumption
            - previous_water["hot"]["kitchen"]["current"]
        )
        cold_bathroom_consumption = (
            self.water.cold_bathroom_consumption
            - previous_water["cold"]["bathroom"]["current"]
        )
        hot_bathroom_consumption = (
            self.water.hot_bathroom_consumption
            - previous_water["hot"]["bathroom"]["current"]
        )

        total_cold_consumption = cold_kitchen_consumption + cold_bathroom_consumption
        total_hot_consumption = hot_kitchen_consumption + hot_bathroom_consumption

        cold_kitchen_cost = cold_kitchen_consumption * self.price.cold
        cold_bathroom_cost = cold_bathroom_consumption * self.price.cold
        hot_kitchen_cost = hot_kitchen_consumption * self.price.hot
        hot_bathroom_cost = hot_bathroom_consumption * self.price.hot

        total_cold_cost = total_cold_consumption * self.price.cold
        total_hot_cost = total_hot_consumption * self.price.hot

        total_cost = total_cold_cost + total_hot_cost

        return {
            "cold": {
                "kitchen": {
                    "current": self.water.cold_kitchen_consumption,
                    "previous": previous_water["cold"]["kitchen"]["current"],
                    "consumption": cold_kitchen_consumption,
                },
                "bathroom": {
                    "current": self.water.cold_bathroom_consumption,
                    "previous": previous_water["cold"]["bathroom"]["current"],
                    "consumption": cold_bathroom_consumption,
                },
                "total_consumption": total_cold_consumption,
            },
            "hot": {
                "kitchen": {
                    "current": self.water.hot_kitchen_consumption,
                    "previous": previous_water["hot"]["kitchen"]["current"],
                    "consumption": hot_kitchen_consumption,
                },
                "bathroom": {
                    "current": self.water.hot_bathroom_consumption,
                    "previous": previous_water["hot"]["bathroom"]["current"],
                    "consumption": hot_bathroom_consumption,
                },
                "total_consumption": total_hot_consumption,
            },
            "cost": {
                "kitchen_cold": cold_kitchen_cost,
                "kitchen_hot": hot_kitchen_cost,
                "bathroom_cold": cold_bathroom_cost,
                "bathroom_hot": hot_bathroom_cost,
                "cold": total_cold_cost,
                "hot": total_hot_cost,
                "total_cost": total_cost,
            },
        }

    def format_for_first_record(self) -> dict:
        return {
            "date": self.date,
            "utilities": {
                "gas": {
                    "current": self.gas.consumption,
                },
                "water": {
                    "cold": {
                        "kitchen": {
                            "current": self.water.cold_kitchen_consumption,
                        },
                        "bathroom": {
                            "current": self.water.cold_bathroom_consumption,
                        },
                    },
                    "hot": {
                        "kitchen": {
                            "current": self.water.hot_kitchen_consumption,
                        },
                        "bathroom": {
                            "current": self.water.hot_bathroom_consumption,
                        },
                    },
                    "electricity": {
                        "t1": {
                            "current": self.electricity.t1_consumption,
                            "t2": {
                                "current": self.electricity.t2_consumption,
                            },
                        },
                    },
                },
                "prices": {
                    "gas": self.price.gas,
                    "gas_distribution": self.price.gas_distribution,
                    "electricity": {"t1": self.price.t1, "t2": self.price.t2},
                    "water": {"cold": self.price.cold, "hot": self.price.hot},
                },
                "cost": {},
            },
        }
