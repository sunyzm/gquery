from gquery.coordinate import Coordinate
from dataclasses import dataclass


@dataclass
class AirportInfo:
    index: int
    iata_code: str
    name: str
    country: str
    coord: Coordinate
    seats: int

    def __str__(self):
        return (
            f"{self.iata_code} ({self.name})\n"
            f"- Coordinates: {self.coord}\n"
            f"- Country: {self.country}\n"
            f"- Annual seats (intl): {self.seats:,}\n"
        )
