from gquery.coordinate import Coordinate
from dataclasses import dataclass
from math import isnan


@dataclass
class CityInfo:
    index: int
    name: str
    population: float
    country: str
    admin: str
    coord: Coordinate
    population_display: str = "NA"

    def __post_init__(self):
        self.population_display = (
            f"{round(self.population):,}"
            if not isnan(self.population)
            else "NA"
        )

    def __str__(self):
        return (
            f"{self.name}\n"
            f"- Coordinates: {self.coord}\n"
            f"- Country: {self.country}\n"
            f"- Administration: {self.admin}\n"
            f"- Population: {self.population_display}"
        )
