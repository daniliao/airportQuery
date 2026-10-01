import json

def load_airports(path="airports.json"):
    with open(path) as f:
        return json.load(f)

def build_code_index(airports):
    return {record["code"]: record for record in airports}

def lookup_by_code(code: str, code_index: dict):
    return code_index.get(code.strip().upper())

def lookup_by_name(name: str, airports: list):
    query = name.strip().casefold()
    matches = [r for r in airports if query in r["name"].casefold()]
    matches.sort(key=lambda r: abs(len(r["name"]) - len(name)))
    return matches
