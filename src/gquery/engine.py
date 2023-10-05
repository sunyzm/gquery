from .city import CityInfo
import os
import pandas as pd

DATA_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "data",
)

CITIES_DATAFILE = os.path.join(DATA_PATH, "worldcities.csv")


class GQueryEngine:
    def __init__(self, datafile_path=CITIES_DATAFILE, debug_enabled=False):
        if not os.path.exists(datafile_path):
            raise FileExistsError(f"File {datafile_path} does not exists")

        df = pd.read_csv(datafile_path, header=0, engine="c")
        df = df.assign(index=df.index)
        df.drop(columns=["iso2", "iso3", "capital", "id"], inplace=True)
        df["city_normalized"] = df["city_ascii"].str.lower()

        self.__worldcity_df = df

        if debug_enabled:
            print("GQueryEngine has been initalized.")

    def get(self, id: int) -> CityInfo | None:
        df = self.__worldcity_df
        matched_rows = df[df.index == id]
        if matched_rows.empty:
            print(f"ERROR: City ID {id} is not valid")
            return None

        city_data = matched_rows.iloc[0].to_dict()
        return CityInfo(city_data)

    def retrieve(self, city_name: str, max_num: int = -1) -> list[CityInfo]:
        df = self.__worldcity_df
        matched_rows = df[df["city_normalized"] == city_name.lower()]
        if matched_rows.empty:
            return []

        matched_cities = [
            CityInfo(row.to_dict()) for _, row in matched_rows.iterrows()
        ]
        return matched_cities[:max_num] if max_num > 0 else matched_cities

    def print(self, city_name: str) -> None:
        matched_cities = self.retrieve(city_name)
        if len(matched_cities) == 0:
            print(f"{city_name} is not found")
        else:
            print(matched_cities[0])
