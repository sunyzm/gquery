from .airport import AirportInfo
from .city import CityInfo
from .coordinate import Coordinate
import os
import pandas as pd

DATA_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "data",
)

CITIES_DATAFILE = os.path.join(DATA_PATH, "worldcities.csv")
AIRPORTS_DATAFILE = os.path.join(DATA_PATH, "global_airports.csv")


class GQueryEngine:
    def __init__(self, debug_enabled=False):
        if not os.path.exists(CITIES_DATAFILE):
            raise FileExistsError(f"File {CITIES_DATAFILE} does not exists")

        if not os.path.exists(AIRPORTS_DATAFILE):
            raise FileExistsError(f"File {AIRPORTS_DATAFILE} does not exists")

        self._city_df = pd.read_csv(CITIES_DATAFILE, header=0, engine="c")
        self._city_df = self._city_df.assign(index=self._city_df.index)
        self._city_df.drop(
            columns=["iso2", "iso3", "capital", "id"], inplace=True
        )
        self._city_df["city_normalized"] = self._city_df[
            "city_ascii"
        ].str.lower()

        self._airport_df = pd.read_csv(AIRPORTS_DATAFILE, header=0, engine="c")
        self._airport_df = self._airport_df.assign(index=self._airport_df.index)

        if debug_enabled:
            print("GQueryEngine has been initalized.")

    def get(self, id: int) -> CityInfo | None:
        df = self._city_df
        matched_rows = df[df.index == id]
        if matched_rows.empty:
            print(f"ERROR: City ID {id} is not valid")
            return None

        city_data = matched_rows.iloc[0].to_dict()
        return CityInfo(city_data)

    def retrieve(self, city_name: str, max_num: int = -1) -> list[CityInfo]:
        df = self._city_df
        matched_rows = df[df["city_normalized"] == city_name.lower()]
        if matched_rows.empty:
            return []

        matched_cities = [
            CityInfo(row.to_dict()) for _, row in matched_rows.iterrows()
        ]
        return matched_cities[:max_num] if max_num > 0 else matched_cities

    def find_airport(self, code: str) -> AirportInfo | None:
        df = self._airport_df
        matched_rows = df[df["Code"] == code.upper()]
        if matched_rows.empty:
            return None

        airport_data = matched_rows.iloc[0].to_dict()
        return AirportInfo(
            index=airport_data["index"],
            iata_code=airport_data["Code"],
            name=airport_data["Name"],
            country=airport_data["Country"],
            coord=Coordinate(
                airport_data["Latitude"], airport_data["Longitude"]
            ),
            seats=int(airport_data["TotalSeats"]),
        )
