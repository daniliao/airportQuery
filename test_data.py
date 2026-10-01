from data import load_airports, build_code_index, lookup_by_code, lookup_by_name

airports = load_airports()
code_index = build_code_index(airports)


def test_load_airports():
    assert len(airports) > 0
    assert "code" in airports[0]
    assert "name" in airports[0]
    assert "altitude" in airports[0]


def test_code_index_built():
    assert len(code_index) > 0
    assert "KSFO" in code_index


def test_lookup_by_code_found():
    record = lookup_by_code("KSFO", code_index)
    assert record is not None
    assert record["name"] == "San Francisco International Airport"
    assert record["altitude"] == 13


def test_lookup_by_code_case_insensitive():
    assert lookup_by_code("ksfo", code_index) is not None
    assert lookup_by_code("  KSFO  ", code_index) is not None


def test_lookup_by_code_not_found():
    assert lookup_by_code("XXXX_FAKE", code_index) is None


def test_lookup_by_name_single_match():
    matches = lookup_by_name("Denver International", airports)
    assert len(matches) >= 1
    assert matches[0]["code"] == "KDEN"


def test_lookup_by_name_substring():
    matches = lookup_by_name("Municipal", airports)
    assert len(matches) > 100
    for m in matches:
        assert "municipal" in m["name"].casefold()


def test_lookup_by_name_case_insensitive():
    upper = lookup_by_name("DENVER INTERNATIONAL", airports)
    lower = lookup_by_name("denver international", airports)
    assert len(upper) == len(lower)


def test_lookup_by_name_no_match():
    matches = lookup_by_name("Fantasy Nonexistent Airport", airports)
    assert len(matches) == 0


def test_lookup_by_name_best_match_first():
    matches = lookup_by_name("La Guardia", airports)
    assert len(matches) >= 1
    assert "La Guardia" in matches[0]["name"]


def test_known_airports():
    cases = {
        "KSFO": ("San Francisco International Airport", 13),
        "KJFK": ("John F Kennedy International Airport", 13),
        "EIDW": ("Dublin Airport", 242),
        "KDEN": ("Denver International Airport", 5431),
        "VABB": ("Chhatrapati Shivaji International Airport", 39),
        "EGLL": ("London Heathrow Airport", 83),
        "KSEA": ("Seattle–Tacoma International Airport", 433),
    }
    for code, (expected_name, expected_alt) in cases.items():
        record = lookup_by_code(code, code_index)
        assert record is not None, f"{code} not found"
        assert record["name"] == expected_name, f"{code}: got {record['name']}"
        assert record["altitude"] == expected_alt, f"{code}: got {record['altitude']}"
