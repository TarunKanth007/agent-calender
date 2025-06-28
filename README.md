# 📅 Conversational AI Calendar Assistant

## 🚀 Project Overview
A smart AI assistant that helps users schedule meetings through natural language conversations. It interacts via a chat interface, understands time-based requests, checks calendar availability, and confirms bookings.

## 💬 Features
- Understands natural language input like “Schedule a meeting tomorrow at 4PM.”
- Supports intent detection: scheduling and checking availability.
- Parses human-friendly time expressions.
- Interacts with Google Calendar to manage events.
- Fully integrated with a user-friendly Streamlit chat interface.

## 🔧 Technology Stack
- **Frontend**: Streamlit
- **Backend**: Python
- **NLP**: Gemini 2.0 Flash API
- **Calendar Integration**: Google Calendar API
- **Date Parsing**: `dateparser` Python library
- **Secrets Management**: Streamlit Secrets (no local `.env` or `.json` files)

## 🔐 Security
- All credentials (API keys, calendar ID, service account) are securely stored using Streamlit’s built-in secrets manager.
- No sensitive files are committed to the repository.

## 📈 Sample Interactions
- “Book a call tomorrow at 3PM”
- “Do I have any free time this Friday?”
- “Schedule a meeting between 3 and 5 PM next week”

## 🌍 Deployment
- Hosted on Streamlit Cloud
- Publicly accessible and secure
- Does not require local environment setup

## 🧠 Future Improvements
- Add support for cancelling and rescheduling events
- Implement user authentication (OAuth)
- Enhance memory using LangGraph for multi-turn dialogue

## ✅ Outcome
A deployable, secure, and intelligent scheduling agent that demonstrates the power of AI, APIs, and modern cloud tools working together seamlessly.
