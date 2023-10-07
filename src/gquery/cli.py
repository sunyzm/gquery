from gquery import AirportInfo, CityInfo, compute_coord_distance, LengthUnit, GQueryEngine
import pyinputplus as pyip
import sys


def find_city(query_engine: GQueryEngine, city_name: str) -> CityInfo | None:
    matched_cities = query_engine.find_cities(city_name)
    if len(matched_cities) == 0:
        print("No matched city is found.")
        return None
    elif len(matched_cities) == 1:
        return matched_cities[0]
    else:
        print("There are multiple matches:")
        for i in range(len(matched_cities)):
            city_info = matched_cities[i]
            print(
                f"{i+1}. {city_info.name} ({city_info.country}, {city_info.admin})"
            )
        selected = pyip.inputInt(
            f"Please select a city [1-{len(matched_cities)}]:",
            default=1,
            min=1,
            max=len(matched_cities) + 1,
        )
        return matched_cities[selected - 1]


def find_place(query_engine: GQueryEngine, name: str) -> AirportInfo | CityInfo | None:
    if matched_airport := query_engine.find_airport(name):
        return matched_airport
    return find_city(query_engine, name)


def main():
    argv = sys.argv
    query_engine = GQueryEngine()

    match argv[1:]:
        case ("info", *names):
            for name in names:
                if matched_place := find_place(query_engine, name):
                    print(matched_place)
        case ("distance", name1, name2, *extra_arg):
            place1 = find_place(query_engine, name1)
            if place1 is None:
                print("Failed to find {name1}")
                exit(1)

            place2 = find_place(query_engine, name2)
            if place2 is None:
                print("Failed to find {name2}")
                exit(1)

            unit = LengthUnit.KM
            for arg in extra_arg:
                if arg.startswith("--unit="):
                    unit_str = arg.split(sep="=", maxsplit=1)[1].lower()
                    match unit_str:
                        case "mi" | "mile":
                            unit = LengthUnit.MI
                        case "km" | "kilometer":
                            unit = LengthUnit.KM
                        case _:
                            print(f"Unrecognized unit {unit}")
                            exit(1)

            distance, unit_symbol = compute_coord_distance(
                place1.coord, place2.coord, unit
            )
            print(
                f"Distance between {place1.name} and "
                f"{place2.name}: {distance:.1f} {unit_symbol}"
            )
        case _:
            print("Unrecognized command")
            exit(1)


if __name__ == "__main__":
    main()
