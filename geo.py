import math
from data import lookup_by_code


def haversine_miles(lat1, lon1, lat2, lon2):
    R = 3958.8
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return R * 2 * math.asin(math.sqrt(a))


def find_airports_within_radius(center_code: str, radius_miles: float, airports: list, code_index: dict):
    center = lookup_by_code(center_code, code_index)
    if not center:
        return None, []
    clat, clon = center["latitude_deg"], center["longitude_deg"]
    results = []
    for r in airports:
        if r["code"] == center["code"]:
            continue
        dist = haversine_miles(clat, clon, r["latitude_deg"], r["longitude_deg"])
        if dist <= radius_miles:
            results.append((r, round(dist, 1)))
    results.sort(key=lambda x: x[1])
    return center, results
