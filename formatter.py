FIELD_LABELS = {
    "name": "Name",
    "code": "Code",
    "altitude": "Altitude",
    "type": "Type",
    "latitude_deg": "Latitude",
    "longitude_deg": "Longitude",
    "continent": "Continent",
    "iso_country": "Country",
    "iso_region": "Region",
    "municipality": "Municipality",
    "scheduled_service": "Scheduled service",
    "gps_code": "GPS code",
    "iata_code": "IATA code",
    "local_code": "Local code",
    "wikipedia_link": "Website",
    "frequency_mhz": "Frequency",
    "runway_length_ft": "Runway length",
    "runway_width_ft": "Runway width",
    "runway_surface": "Runway surface",
    "runway_lighted": "Runway lighted",
    "runway_closed": "Runway closed",
}

FIELD_UNITS = {
    "altitude": "ft",
    "frequency_mhz": "MHz",
    "runway_length_ft": "ft",
    "runway_width_ft": "ft",
    "latitude_deg": "°",
    "longitude_deg": "°",
}


def format_value(field: str, val) -> str:
    if val is None or val == "":
        return "N/A"
    unit = FIELD_UNITS.get(field, "")
    if unit:
        return f"{val} {unit}"
    return str(val)


def format_answer(record: dict, fields: list[str]) -> str:
    if sorted(fields) == sorted(["name", "code", "altitude"]):
        return (f"{record['name']} ({record['code']}) has an altitude of "
                f"{record['altitude']} ft.")
    if len(fields) == 1:
        f = fields[0]
        label = FIELD_LABELS.get(f, f)
        val = format_value(f, record.get(f))
        return f"{label} for {record['name']} ({record['code']}): {val}"
    parts = []
    for f in fields:
        label = FIELD_LABELS.get(f, f)
        val = format_value(f, record.get(f))
        parts.append(f"{label}: {val}")
    return f"{record['name']} ({record['code']}) — " + ", ".join(parts)


def format_multi_match(lookup_value: str, records: list[dict]) -> str:
    lines = [f"Found {len(records)} airports matching \"{lookup_value}\":"]
    for r in records:
        lines.append(f"  - {r['name']} ({r['code']}), altitude: {r['altitude']} ft")
    return "\n".join(lines)


def format_radius_results(center: dict, radius: float, nearby: list) -> str:
    if not nearby:
        return f"No airports found within {radius} miles of {center['name']} ({center['code']})."
    airport_lines = [f"  - {r['name']} ({r['code']}): {dist} miles away" for r, dist in nearby[:20]]
    answer = f"Airports within {radius} miles of {center['name']} ({center['code']}):\n" + "\n".join(airport_lines)
    if len(nearby) > 20:
        answer += f"\n  ...and {len(nearby) - 20} more."
    return answer
