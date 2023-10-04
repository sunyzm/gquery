from gquery.coordinate import decimal_to_degree, Coordinate


def test_decimal_to_degree():
    assert decimal_to_degree(37.5, "N") == "37° 30' N"
    assert decimal_to_degree(22.0, "W") == "22° 0' W"


def test_print_coordinate():
    assert Coordinate(lat=37.5, lng=-22.2).__str__() == "37° 30' N, 22° 12' W"
