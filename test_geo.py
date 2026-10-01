import math
from geo import haversine_miles, find_airports_within_radius
from data import load_airports, build_code_index

airports = load_airports()
code_index = build_code_index(airports)


def test_haversine_same_point():
    assert haversine_miles(37.0, -122.0, 37.0, -122.0) == 0.0


def test_haversine_known_distance():
    # SFO (37.619, -122.375) to OAK (37.721, -122.221) ~= 11 miles
    dist = haversine_miles(37.619, -122.375, 37.721, -122.221)
    assert 9 < dist < 13


def test_haversine_long_distance():
    # SFO to JFK ~= 2586 miles
    dist = haversine_miles(37.619, -122.375, 40.6398, -73.7789)
    assert 2500 < dist < 2700


def test_haversine_symmetry():
    d1 = haversine_miles(37.0, -122.0, 40.0, -73.0)
    d2 = haversine_miles(40.0, -73.0, 37.0, -122.0)
    assert math.isclose(d1, d2)


def test_find_within_radius():
    center, nearby = find_airports_within_radius("KSFO", 15.0, airports, code_index)
    assert center is not None
    assert center["code"] == "KSFO"
    assert len(nearby) > 0
    codes = [r["code"] for r, _ in nearby]
    assert "KSFO" not in codes  # center excluded
    for _, dist in nearby:
        assert dist <= 15.0


def test_find_within_radius_sorted():
    _, nearby = find_airports_within_radius("KSFO", 25.0, airports, code_index)
    distances = [dist for _, dist in nearby]
    assert distances == sorted(distances)


def test_find_within_radius_not_found():
    center, nearby = find_airports_within_radius("XXXX_FAKE", 10.0, airports, code_index)
    assert center is None
    assert nearby == []


def test_find_within_radius_zero():
    center, nearby = find_airports_within_radius("KSFO", 0.0, airports, code_index)
    assert center is not None
    assert len(nearby) == 0
