# Airport Chatbot

A chatbot that lets you ask questions about airports in plain English. It uses `gpt-3.5-turbo` to understand what you're asking, then looks up the answer from a dataset of 75,000+ airports.

The LLM figures out what you're asking. The actual data comes from `airports.json`. This keeps answers accurate.

## How it works

When you type a question, here's what happens:

1. Your message gets sent to `gpt-3.5-turbo` with a prompt that says "figure out what airport and what info this person wants"
2. The model responds with structured data, like `lookup_type: code, lookup_value: KSFO, fields: ["frequency_mhz"]`
3. We parse that, look up the airport in our JSON file, grab the right fields, and format a response

The conversation history gets passed along each time so the model can handle follow-ups like "what city is *it* in?"

## Project structure

| File | What it does |
|------|-------------|
| `main.py` | The REPL — you run this and start chatting |
| `data.py` | Loads the JSON and has the two lookup functions |
| `classifier.py` | Talks to the LLM to understand the user's question |
| `formatter.py` | Turns raw data into readable responses |
| `geo.py` | Distance math for "airports near X" queries |

## Getting started

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Drop `airports.json` into the project folder (it's ~40MB so it's not in the repo).

Set your OpenAI key:

```bash
export OPENAI_API_KEY=your-key-here
```

Then just run it:

```bash
python3 main.py
```

## What it can do

### Look up by code or name

You can ask about an airport using its code or its name. If the name matches multiple airports, it lists all of them.

```
user: Can you tell me about KSFO?
assistant: San Francisco International Airport (KSFO) has an altitude of 13 ft.

user: Tell me about denver international
assistant: Denver International Airport (KDEN) has an altitude of 5431 ft.

user: Municipal
assistant: Found 1453 airports matching "Municipal":
  - Ely Municipal Airport (KELO), altitude: 1456 ft
  - Roy Municipal Airport (US-7102), altitude: 5895 ft
  ...
```

### Ask about any field

Frequency, municipality, website, runway info, whatever's in the data.

```
user: What frequency can I contact KSFO on?
assistant: Frequency for San Francisco International Airport (KSFO): 125.35 MHz

user: What municipality is it in?
assistant: Municipality for San Francisco International Airport (KSFO): San Francisco

user: What is the website for La Guardia Airport?
assistant: Website for La Guardia Airport (KLGA): https://en.wikipedia.org/wiki/LaGuardia_Airport
```

Notice the follow-up — "What municipality is *it* in?" knows "it" means KSFO because we keep conversation history.

### Find nearby airports

Uses the haversine formula to calculate real distances between coordinates.

```
user: Which airports are within 25 miles of KSFO?
assistant: Airports within 25.0 miles of San Francisco International Airport (KSFO):
  - Coast Guard Air Station San Francisco (US-0188): 1.2 miles away
  - San Carlos Airport (KSQL): 10.1 miles away
  - Metropolitan Oakland International Airport (KOAK): 11.0 miles away
  ...
```

## The two lookup functions

These are the core "tools" the chatbot uses:

- **`lookup_by_code("KSFO")`** — exact match against `record.code`. We build a dictionary at startup so this is instant.
- **`lookup_by_name("municipal")`** — checks if the input appears anywhere in the airport name, case-insensitive. Returns every match.

## Running tests

```bash
python3 -m pytest -v
```
