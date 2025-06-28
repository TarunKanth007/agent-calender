import streamlit as st
from backend.calendar_service import book_event, check_free_slots
from backend.nlp_utils import extract_intent_and_entities
import dateparser

st.set_page_config(page_title="Calendar Assistant", page_icon="📅")
st.title("🤖 Calendar Booking Assistant")

st.markdown("Ask me to schedule meetings or check availability. Example:")
st.code("Schedule a call tomorrow at 4PM", language="markdown")

user_input = st.text_input("👤 You", key="user_input")

if user_input:
    with st.spinner("Thinking..."):
        try:
            intent, entities = extract_intent_and_entities(user_input)

            if intent == "schedule":
                summary = entities.get("summary", "Meeting")
                start = dateparser.parse(entities.get("start_time"))
                end = dateparser.parse(entities.get("end_time"))

                if start and end:
                    event_link = book_event(summary, start, end)
                    st.success(f"📅 Event created: [Open in Calendar]({event_link})")
                else:
                    st.error("❌ I couldn't understand the time. Please rephrase.")

            elif intent == "check_availability":
                date_str = entities.get("date")
                if not date_str:
                    st.error("❌ Please specify a day to check availability.")
                else:
                    try:
                        date = dateparser.parse(date_str)
                        if not date:
                            raise ValueError("Invalid date format.")
                        slots = check_free_slots(date)
                        if slots:
                            response = "🕒 Available slots:\n" + "\n".join(
                                [f"{start.strftime('%I:%M %p')} - {end.strftime('%I:%M %p')}" for start, end in slots]
                            )
                        else:
                            response = "😔 No free slots found."
                        st.success(response)
                    except Exception as e:
                        st.error(f"❌ Error checking availability: {e}")
            else:
                st.error("❌ I didn't understand your request. Try saying something like 'Schedule a call tomorrow at 4PM'.")

        except Exception as e:
            st.error(str(e))
