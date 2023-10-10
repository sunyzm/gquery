from gquery import (
    AirportInfo,
    CityInfo,
    compute_coord_distance,
    LengthUnit,
    GQueryEngine,
)
import click
import pyinputplus as pyip


_query_engine = GQueryEngine()


def find_city(query_engine: GQueryEngine, city_name: str) -> CityInfo | None:
    matched_cities = query_engine.find_cities(city_name)
    if len(matched_cities) == 0:
        return None
    elif len(matched_cities) == 1:
        return matched_cities[0]
    else:
        print("There are multiple matches:")
        for i in range(len(matched_cities)):
            city_info = matched_cities[i]
            print(f"{i+1}. {city_info.name} ({city_info.country}, {city_info.admin})")
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


def get_distance_unit(unit: str) -> LengthUnit:
    match unit:
        case "mi" | "mile":
            return LengthUnit.MI
        case "km" | "kilometer":
            return LengthUnit.KM
        case _:
            print(f"Unrecognized unit {unit}")
            exit(1)


@click.group()
def cli():
    pass


@click.command()
@click.argument("names", nargs=-1)
def info(names):
    for name in names:
        if matched_place := find_place(_query_engine, name):
            print(matched_place)


@click.command()
@click.argument("names", nargs=2)
@click.option("--unit", default="km", type=str, help="Unit of distance (km or mi)")
def distance(names, unit):
    place1 = find_place(_query_engine, names[0])
    if place1 is None:
        print(f"Failed to find {names[0]}")
        exit(1)

    place2 = find_place(_query_engine, names[1])
    if place2 is None:
        print(f"Failed to find {names[1]}")
        exit(1)

    distance_unit = get_distance_unit(unit)
    distance, unit_symbol = compute_coord_distance(
        place1.coord, place2.coord, distance_unit
    )
    print(
        f"Distance between {place1.name} and "
        f"{place2.name}: {distance:.1f} {unit_symbol}"
    )


@click.command()
@click.argument("name")
@click.option("--num", default=1, type=int)
@click.option("--unit", default="km", type=str, help="Unit of distance (km or mi)")
def nearby_airports(name, num, unit):
    city = find_city(_query_engine, name)
    if city is None:
        print(f"Failed to find city {name}")
        exit(1)

    distance_unit = get_distance_unit(unit)
    for airport in _query_engine.find_nearest_airports(city.coord, num=num):
        print(airport)
        distance, unit = compute_coord_distance(
            city.coord, airport.coord, distance_unit
        )
        print(f"Distance to {city.name}: {distance} {unit}\n")


cli.add_command(info)
cli.add_command(distance)
cli.add_command(nearby_airports, name="nearby-airports")


def main():
    cli()
