# pages/client_action.py

import streamlit as st
import psycopg2, os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
DB_URL = os.getenv("DATABASE_URL")

# grab the query-params
params    = st.experimental_get_query_params()
client_id = params.get("client_id", [""])[0]
action    = params.get("action",    [""])[0]

if not client_id or not action:
    st.error("Missing client_id or action in the URL.")
    st.stop()

st.title(f"{action.title()} for Client {client_id}")

# build the form dynamically
with st.form("action_form"):
    if action == "requirement":
        reqs = st.text_area("Enter client requirements")
    elif action == "schedule":
        date = st.date_input("Choose a date")
        time = st.time_input("Choose a time")
    elif action == "dead":
        reason = st.text_area("Reason for marking dead")
    submitted = st.form_submit_button("Submit")

if submitted:
    try:
        conn = psycopg2.connect(DB_URL, sslmode="require")
        cur  = conn.cursor()
        if action == "requirement":
            cur.execute(
                "INSERT INTO client_requirements(client_id, requirements, created_on) VALUES (%s,%s,%s)",
                (client_id, reqs, datetime.utcnow())
            )
        elif action == "schedule":
            cur.execute(
                "INSERT INTO client_schedule(client_id, sched_date, sched_time) VALUES (%s,%s,%s)",
                (client_id, date, time)
            )
        else:  # dead
            cur.execute(
                "INSERT INTO client_dead(client_id, reason, created_on) VALUES (%s,%s,%s)",
                (client_id, reason, datetime.utcnow())
            )
        conn.commit()
        cur.close()
        conn.close()
        st.success("Saved successfully!")
    except Exception as e:
        st.error(f"Database error: {e}")
