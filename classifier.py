import json
from openai import OpenAI

CLASSIFY_SYSTEM = """You are a query classifier for an airport database.

Given the user's message and conversation history, extract:
1. lookup_type: "code" if the user provides an airport code (like KSFO, KJFK), "name" if they provide an airport name, or "none" if they are asking a follow-up about a previously mentioned airport.
2. lookup_value: the airport code or name substring the user mentioned. If this is a follow-up (lookup_type=none), leave empty.
3. fields: a JSON list of field names the user is asking about. Use these exact field names when applicable: name, code, altitude, type, latitude_deg, longitude_deg, continent, iso_country, iso_region, municipality, scheduled_service, gps_code, iata_code, local_code, wikipedia_link, frequency_mhz, runway_length_ft, runway_width_ft, runway_surface, runway_lighted, runway_closed. If the user asks generally ("tell me about"), use ["name", "code", "altitude"]. Map natural language to field names (e.g. "frequency" -> "frequency_mhz", "website" or "link" or "url" -> "wikipedia_link", "city" -> "municipality").
4. radius_query: true if the user is asking about airports within a distance of another airport, false otherwise.
5. radius_miles: if radius_query is true, the radius in miles.

Respond in EXACTLY this format, one field per line:
lookup_type: <code|name|none>
lookup_value: <value>
fields: <JSON list>
radius_query: <true|false>
radius_miles: <number or empty>"""


def chat(client: OpenAI, messages: list[dict]) -> str:
    resp = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0,
    )
    return resp.choices[0].message.content.strip()


def classify(client: OpenAI, conversation_history: list[dict]) -> dict:
    messages = [{"role": "system", "content": CLASSIFY_SYSTEM}] + conversation_history
    raw = chat(client, messages)
    result = {}
    for line in raw.splitlines():
        if ":" in line:
            key, val = line.split(":", 1)
            result[key.strip()] = val.strip()
    return result


def parse_fields(fields_raw: str) -> list[str]:
    try:
        return json.loads(fields_raw)
    except json.JSONDecodeError:
        return ["name", "code", "altitude"]
