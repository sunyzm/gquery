from dataclasses import dataclass
from enum import Enum
from math import radians, cos, sin, asin, sqrt, floor


def decimal_to_degree(val: float, direction: str) -> str:
    abs_val = abs(val)
    degree = floor(abs_val)
    minute = abs_val - degree
    return f"{degree}{chr(176)} {round(minute*60.0)}' {direction}"


@dataclass(frozen=True)
class Coordinate:
    lat: float
    lng: float

    def __str__(self):
        return (
            f"{decimal_to_degree(self.lat, ('N' if self.lat >= 0 else 'S'))}, "
            f"{decimal_to_degree(self.lng, ('E' if self.lng >= 0 else 'W'))}"
        )

    def __iter__(self):
        return (v for v in (self.lat, self.lng))

    def __eq__(self, other):
        return tuple(self) == tuple(other)


class LengthUnit(Enum):
    KM = 1
    MI = 2


def coord_distance(
    lat1, lat2, lon1, lon2, unit: LengthUnit = LengthUnit.KM
) -> tuple[float, str]:
    # Convert from degrees to radians.
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2

    c = 2 * asin(sqrt(a))

    use_mile = unit == LengthUnit.MI
    # Radius of earth.
    r = 3958.8 if use_mile else 6371

    return c * r, "mi" if use_mile else "km"


def compute_coord_distance(
    coord1: Coordinate, coord2: Coordinate, unit: LengthUnit = LengthUnit.KM
) -> tuple[float, str]:
    return coord_distance(
        coord1.lat,
        coord2.lat,
        coord1.lng,
        coord2.lng,
        unit,
    )
