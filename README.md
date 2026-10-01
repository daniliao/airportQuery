# Airport Chatbot

An LLM-powered chatbot that answers natural language queries about airports using a 75,000-record dataset.

## Architecture

The LLM (gpt-3.5-turbo) interprets natural language queries. The JSON dataset answers factual questions. This separation ensures accurate data while allowing flexible input.

```
User query → LLM classifier (1 API call) → local data lookup → formatted response
```

### Modules

| File | Purpose |
|------|---------|
| `main.py` | Interactive REPL loop |
| `data.py` | Data loading and lookup functions |
| `classifier.py` | LLM query classification |
| `formatter.py` | Response formatting |
| `geo.py` | Haversine distance and radius search |

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Place `airports.json` in the project root (not included in repo due to size).

Set your API key:

```bash
export OPENAI_API_KEY=sk-proj-your-key-here
```

## Usage

```bash
python3 main.py
```

### Example queries

```
user: Can you tell me about KSFO?
assistant: San Francisco International Airport (KSFO) has an altitude of 13 ft.

user: What frequency can I contact KSFO on?
assistant: Frequency for San Francisco International Airport (KSFO): 125.35 MHz

user: What municipality is it in?
assistant: Municipality for San Francisco International Airport (KSFO): San Francisco

user: Municipal
assistant: Found 1453 airports matching "Municipal":
  - Ely Municipal Airport (KELO), altitude: 1456 ft
  ...

user: Which airports are within 25 miles of KSFO?
assistant: Airports within 25.0 miles of San Francisco International Airport (KSFO):
  - Coast Guard Air Station San Francisco (US-0188): 1.2 miles away
  ...
```

## Tests

```bash
python3 -m pytest -v
```

## Features

- **Code lookup**: exact match via hash map (O(1))
- **Name search**: case-insensitive substring match, returns all matches
- **Arbitrary field queries**: frequency, municipality, website, runway info, etc.
- **Conversation context**: follow-up questions ("What municipality is *it* in?")
- **Radius search**: find airports within N miles using haversine distance
