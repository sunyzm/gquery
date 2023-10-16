from gquery import (
    AirportInfo,
    CityInfo,
    compute_coord_distance,
    LengthUnit,
    Distance,
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
    match unit.lower():
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
@click.argument("names", nargs=-1)
@click.option("--unit", default="km", type=str, help="Unit of distance (km or mi)")
def distance(names, unit):
    if len(names) < 2:
        print("At least two places are required")
        exit(1)

    places = []
    for name in names:
        if (place := find_place(_query_engine, name)) is None:
            print(f"Failed to find {name}")
            exit(1)
        places.append(place)

    distance_unit = get_distance_unit(unit)

    total_distance = Distance(0, distance_unit)
    for i in range(len(places) - 1):
        distance = compute_coord_distance(
            places[i].coord, places[i + 1].coord, distance_unit
        )
        total_distance += distance
        print(
            f"Distance between {places[i].name} and " f"{places[i+1].name}: {distance}"
        )

    if len(places) > 2:
        print(f"* Total distance: {total_distance}")


@click.command()
@click.argument("name")
@click.option("--num", default=1, type=int)
@click.option("--unit", default="km", type=str, help="Unit of distance (km or mi)")
@click.option("--maxdist", default=-1.0, type=float, help="Maximum distance to search")
def nearby_airports(name, num, unit, maxdist):
    place = find_place(_query_engine, name)
    if place is None:
        print(f"Failed to find {name}")
        exit(1)

    distance_unit = get_distance_unit(unit)
    search_radius = Distance(maxdist, distance_unit)
    excluded_codes = set()
    if isinstance(place, AirportInfo):
        excluded_codes.add(place.iata_code)

    airports = _query_engine.find_nearest_airports(
        place.coord,
        num=num,
        search_radius=search_radius.to_km().value,
        excluded_codes=excluded_codes,
    )
    if len(airports) == 0:
        print("No matching airport")
    for i in range(len(airports)):
        airport = airports[i]
        print(f"{i+1}.", airport)
        distance = compute_coord_distance(place.coord, airport.coord, distance_unit)
        print(f"Distance to {place.name}: {distance}\n")


cli.add_command(info)
cli.add_command(distance)
cli.add_command(nearby_airports, name="nearby-airports")


def main():
    cli()
