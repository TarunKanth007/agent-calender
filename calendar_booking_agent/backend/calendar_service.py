import os
import json
import pytz
import streamlit as st
from datetime import datetime, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build

# Load credentials from Streamlit secrets
creds_data = json.loads(st.secrets["GOOGLE_CREDENTIALS_FILE"])
GOOGLE_CALENDAR_ID = st.secrets["GOOGLE_CALENDAR_ID"]

# Authenticate with Google
credentials = service_account.Credentials.from_service_account_info(
    creds_data,
    scopes=["https://www.googleapis.com/auth/calendar"]
)

service = build("calendar", "v3", credentials=credentials)

def book_event(summary: str, start_time: datetime, end_time: datetime):
    event = {
        "summary": summary,
        "start": {"dateTime": start_time.isoformat(), "timeZone": "UTC"},
        "end": {"dateTime": end_time.isoformat(), "timeZone": "UTC"},
    }

    created_event = service.events().insert(calendarId=GOOGLE_CALENDAR_ID, body=event).execute()
    return created_event.get("htmlLink")

def list_events(day: datetime):
    start_of_day = day.replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + "Z"
    end_of_day = (day + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0).isoformat() + "Z"

    events_result = service.events().list(
        calendarId=GOOGLE_CALENDAR_ID,
        timeMin=start_of_day,
        timeMax=end_of_day,
        singleEvents=True,
        orderBy="startTime"
    ).execute()

    return events_result.get("items", [])

def check_free_slots(day: datetime):
    events = list_events(day)

    busy_slots = []
    for event in events:
        start = event.get("start", {}).get("dateTime")
        end = event.get("end", {}).get("dateTime")
        if start and end:
            busy_slots.append((start, end))

    busy_slots.sort(key=lambda x: x[0])

    work_start = day.replace(hour=9, minute=0, second=0, microsecond=0)
    work_end = day.replace(hour=17, minute=0, second=0, microsecond=0)

    free_slots = []
    current = work_start

    for slot in busy_slots:
        try:
            start = datetime.fromisoformat(slot[0])
            end = datetime.fromisoformat(slot[1])
            if current < start:
                free_slots.append((current, start))
            current = max(current, end)
        except Exception as e:
            print("❌ Error parsing busy slot:", e)

    if current < work_end:
        free_slots.append((current, work_end))

    return free_slots
