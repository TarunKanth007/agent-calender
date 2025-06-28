import streamlit as st
import json
import requests
from datetime import datetime

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

def extract_intent_and_entities(user_input: str):
    now = datetime.utcnow().replace(microsecond=0).isoformat() + "Z"

    prompt = f"""
You are a smart calendar assistant.

Current UTC time: {now}
User said: \"{user_input}\"

Extract intent and event data as valid JSON.

If the user wants to schedule, return:
{{
  "intent": "schedule",
  "summary": "Call",
  "start_time": "2025-06-28T16:00:00Z",
  "end_time": "2025-06-28T17:00:00Z"
}}

If the user asks about availability, return:
{{
  "intent": "check_availability",
  "date": "2025-06-28"
}}

Resolve relative time phrases like "tomorrow afternoon", "next Friday", or "this weekend" into exact UTC datetimes in ISO 8601 format.
Respond only with JSON and nothing else.
"""

    payload = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    try:
        response = requests.post(GEMINI_URL, headers={"Content-Type": "application/json"}, json=payload)
        response.raise_for_status()
        candidates = response.json().get("candidates", [])
        text = candidates[0]["content"]["parts"][0]["text"].strip() if candidates else ""

        if text.startswith("```json"):
            text = text[7:].split("```")[0].strip()
        elif text.startswith("```"):
            text = text[3:].split("```")[0].strip()

        parsed = json.loads(text)
        return parsed.get("intent"), parsed

    except Exception as e:
        print("❌ Gemini parsing error:", e)
        return None, {}
