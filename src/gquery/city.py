from .coordinate import Coordinate
from dataclasses import dataclass
from math import isnan
from typing import Any, Mapping


@dataclass
class CityInfo:
    index: int
    name: str
    population: float
    population_display: str
    country: str
    admin: str
    coord: Coordinate

    def __init__(self, city_data: Mapping[str, Any]):
        self.index = city_data["index"]
        self.name = city_data["city"]
        self.population = city_data["population"]
        self.population_display = (
            f"{round(self.population):,}"
            if not isnan(self.population)
            else "NA"
        )
        self.country = city_data["country"]
        self.admin = city_data["admin_name"]
        self.coord = Coordinate(city_data["lat"], city_data["lng"])

    def __str__(self):
        return (
            f"{self.name}\n"
            f"- Coordinates: {self.coord}\n"
            f"- Country: {self.country}\n"
            f"- Administration: {self.admin}\n"
            f"- Population: {self.population_display}"
            # f"\n- Index: {self.index}"
        )
