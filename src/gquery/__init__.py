# read version from installed package
from importlib.metadata import version

__version__ = version("gquery")

from gquery import data
from gquery.airport import AirportInfo
from gquery.city import CityInfo
from gquery.coordinate import Coordinate, LengthUnit, compute_coord_distance
from gquery.engine import GQueryEngine
