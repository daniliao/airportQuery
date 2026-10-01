import os
import json
from openai import OpenAI
from data import load_airports, build_code_index, lookup_by_code, lookup_by_name
from classifier import classify, parse_fields
from formatter import format_answer, format_multi_match, format_radius_results
from geo import find_airports_within_radius


def main():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: set the OPENAI_API_KEY environment variable.")
        return
    client = OpenAI(api_key=api_key)
    airports = load_airports()
    code_index = build_code_index(airports)

    print("Airport Chatbot (type 'quit' to exit)")
    print("=" * 40)

    conversation_history = []
    current_airport = None

    while True:
        user_input = input("\nuser: ").strip()
        if user_input.lower() in ("quit", "exit", "q"):
            break
        if not user_input:
            continue

        conversation_history.append({"role": "user", "content": user_input})

        classification = classify(client, conversation_history)
        lookup_type = classification.get("lookup_type", "")
        lookup_value = classification.get("lookup_value", "")
        fields = parse_fields(classification.get("fields", "[]"))
        is_radius = classification.get("radius_query", "false").lower() == "true"

        if is_radius:
            try:
                radius = float(classification.get("radius_miles", "25"))
            except (ValueError, TypeError):
                radius = 25.0

            center_code = lookup_value.upper() if lookup_value else (current_airport["code"] if current_airport else "")
            center, nearby = find_airports_within_radius(center_code, radius, airports, code_index)
            if not center:
                answer = f"Could not find airport with code {center_code}."
            else:
                answer = format_radius_results(center, radius, nearby)
            print(f"assistant: {answer}")
            conversation_history.append({"role": "assistant", "content": answer})
            continue

        record = None
        records = []
        if lookup_type == "code" and lookup_value:
            record = lookup_by_code(lookup_value, code_index)
            if record:
                records = [record]
        elif lookup_type == "name" and lookup_value:
            records = lookup_by_name(lookup_value, airports)
            record = records[0] if records else None
        elif lookup_type == "none" and current_airport:
            record = current_airport
            records = [record]

        if not record:
            answer = "I couldn't find that airport in the database."
            print(f"assistant: {answer}")
            conversation_history.append({"role": "assistant", "content": answer})
            continue

        is_general = sorted(fields) == sorted(["name", "code", "altitude"])
        if len(records) > 1 and is_general:
            current_airport = records[0]
            answer = format_multi_match(lookup_value, records)
            print(f"assistant: {answer}")
            conversation_history.append({"role": "assistant", "content": answer})
            continue

        current_airport = record

        answer = format_answer(record, fields)
        print(f"assistant: {answer}")
        conversation_history.append({"role": "assistant", "content": answer})


if __name__ == "__main__":
    main()
