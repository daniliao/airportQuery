from formatter import format_value, format_answer, format_multi_match, format_radius_results

SAMPLE_RECORD = {
    "name": "San Francisco International Airport",
    "code": "KSFO",
    "altitude": 13,
    "frequency_mhz": 125.35,
    "municipality": "San Francisco",
    "wikipedia_link": "https://en.wikipedia.org/wiki/SFO",
    "home_link": "",
    "runway_length_ft": 11870,
}


def test_format_value_with_unit():
    assert format_value("altitude", 13) == "13 ft"
    assert format_value("frequency_mhz", 125.35) == "125.35 MHz"
    assert format_value("runway_length_ft", 11870) == "11870 ft"


def test_format_value_no_unit():
    assert format_value("municipality", "San Francisco") == "San Francisco"
    assert format_value("name", "Test Airport") == "Test Airport"


def test_format_value_empty():
    assert format_value("home_link", "") == "N/A"
    assert format_value("home_link", None) == "N/A"


def test_format_answer_general():
    result = format_answer(SAMPLE_RECORD, ["name", "code", "altitude"])
    assert "San Francisco International Airport" in result
    assert "KSFO" in result
    assert "13 ft" in result


def test_format_answer_general_any_order():
    result = format_answer(SAMPLE_RECORD, ["altitude", "name", "code"])
    assert "13 ft" in result


def test_format_answer_single_field():
    result = format_answer(SAMPLE_RECORD, ["frequency_mhz"])
    assert "Frequency" in result
    assert "125.35 MHz" in result
    assert "KSFO" in result


def test_format_answer_single_field_municipality():
    result = format_answer(SAMPLE_RECORD, ["municipality"])
    assert "Municipality" in result
    assert "San Francisco" in result


def test_format_answer_single_field_empty():
    result = format_answer(SAMPLE_RECORD, ["home_link"])
    assert "N/A" in result


def test_format_answer_multiple_fields():
    result = format_answer(SAMPLE_RECORD, ["municipality", "altitude"])
    assert "Municipality" in result
    assert "San Francisco" in result
    assert "Altitude" in result
    assert "13 ft" in result


def test_format_multi_match():
    records = [
        {"name": "Airport A", "code": "AA", "altitude": 100},
        {"name": "Airport B", "code": "BB", "altitude": 200},
    ]
    result = format_multi_match("Airport", records)
    assert "Found 2 airports" in result
    assert "Airport A (AA)" in result
    assert "Airport B (BB)" in result
    assert "100 ft" in result
    assert "200 ft" in result


def test_format_radius_results_empty():
    center = {"name": "Test Airport", "code": "TEST"}
    result = format_radius_results(center, 10.0, [])
    assert "No airports found" in result


def test_format_radius_results():
    center = {"name": "Test Airport", "code": "TEST"}
    nearby = [
        ({"name": "Nearby A", "code": "NA"}, 5.2),
        ({"name": "Nearby B", "code": "NB"}, 8.7),
    ]
    result = format_radius_results(center, 10.0, nearby)
    assert "Nearby A (NA): 5.2 miles" in result
    assert "Nearby B (NB): 8.7 miles" in result


def test_format_radius_truncation():
    center = {"name": "Test", "code": "T"}
    nearby = [({"name": f"A{i}", "code": f"C{i}"}, float(i)) for i in range(25)]
    result = format_radius_results(center, 100.0, nearby)
    assert "...and 5 more" in result
