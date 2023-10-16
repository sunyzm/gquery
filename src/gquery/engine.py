from gquery.airport import AirportInfo
from gquery.city import CityInfo
from gquery.coordinate import Coordinate, compute_coord_distance
from gquery.distance import Distance
import gquery
from importlib import resources
from typing import Any, Mapping
import pandas as pd


def _convert_city_data(csv_data: Mapping[str, Any]) -> CityInfo:
    return CityInfo(
        index=csv_data["index"],
        name=csv_data["city"],
        population=csv_data["population"],
        country=csv_data["country"],
        admin=csv_data["admin_name"],
        coord=Coordinate(csv_data["lat"], csv_data["lng"]),
    )


def _convert_airport_data(csv_data: Mapping[str, Any]) -> AirportInfo:
    return AirportInfo(
        index=csv_data["index"],
        iata_code=csv_data["Code"],
        name=csv_data["Name"],
        country=csv_data["Country"],
        coord=Coordinate(csv_data["Latitude"], csv_data["Longitude"]),
        seats=int(csv_data["TotalSeats"]),
    )


class GQueryEngine:
    def __init__(self, debug_enabled=False):
        with resources.as_file(
            resources.files(gquery.data).joinpath("worldcities.csv")
        ) as city_datafile:
            self._city_df = pd.read_csv(city_datafile, header=0, engine="c")
            self._city_df = self._city_df.assign(index=self._city_df.index)
            self._city_df.drop(columns=["iso2", "iso3", "capital", "id"], inplace=True)
            self._city_df["city_normalized"] = self._city_df["city_ascii"].str.lower()

        with resources.as_file(
            resources.files(gquery.data).joinpath("global_airports.csv")
        ) as airport_datafile:
            self._airport_df = pd.read_csv(airport_datafile, header=0, engine="c")
            self._airport_df = self._airport_df.assign(index=self._airport_df.index)

        if debug_enabled:
            print("GQueryEngine has been initalized.")

    def get_city(self, id: int) -> CityInfo | None:
        df = self._city_df
        matched_rows = df[df.index == id]
        if matched_rows.empty:
            print(f"ERROR: City ID {id} is not valid")
            return None

        city_data = matched_rows.iloc[0].to_dict()
        return _convert_city_data(city_data)

    def find_cities(self, city_name: str, max_num: int = -1) -> list[CityInfo]:
        df = self._city_df
        matched_rows = df[df["city_normalized"] == city_name.lower()]
        if matched_rows.empty:
            return []

        matched_cities = [
            _convert_city_data(row.to_dict()) for _, row in matched_rows.iterrows()
        ]

        return matched_cities[:max_num] if max_num > 0 else matched_cities

    def get_airport(self, id: int) -> AirportInfo | None:
        df = self._airport_df
        matched_rows = df[df.index == id]
        if matched_rows.empty:
            print(f"ERROR: Airport ID {id} is not valid")
            return None

        airport_data = matched_rows.iloc[0].to_dict()
        return _convert_airport_data(airport_data)

    def find_airport(self, code: str) -> AirportInfo | None:
        df = self._airport_df
        matched_rows = df[df["Code"] == code.upper()]
        if matched_rows.empty:
            return None

        airport_data = matched_rows.iloc[0].to_dict()
        return _convert_airport_data(airport_data)

    def iter_airports(self):
        for _, data in self._airport_df.iterrows():
            yield _convert_airport_data(data.to_dict())

    def find_nearest_airports(
        self,
        loc: Coordinate,
        num: int = 1,
        search_radius: float = -1.0,
        excluded_codes: set[str] = set(),
    ) -> list[AirportInfo]:
        airport_and_distance = []
        for airport in self.iter_airports():
            if airport.iata_code in excluded_codes:
                continue
            distance = compute_coord_distance(loc, airport.coord)
            if search_radius <= 0 or distance.value <= search_radius:
                airport_and_distance.append((airport, distance))

        airport_and_distance.sort(key=lambda x: x[1].value)
        return [airport for airport, _ in airport_and_distance[:num]]
