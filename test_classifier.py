from classifier import parse_fields


def test_parse_fields_valid():
    assert parse_fields('["name", "code", "altitude"]') == ["name", "code", "altitude"]


def test_parse_fields_single():
    assert parse_fields('["frequency_mhz"]') == ["frequency_mhz"]


def test_parse_fields_invalid():
    assert parse_fields("not json") == ["name", "code", "altitude"]


def test_parse_fields_empty_string():
    assert parse_fields("") == ["name", "code", "altitude"]
