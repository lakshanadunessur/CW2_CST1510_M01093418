import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import streamlit as st
import pandas as pd
import numpy as np
from app.data.db import connect_database
from app.data.users import get_user_by_username, insert_user
from app.data.incidents import (
    get_all_incidents,
    insert_incident,
    update_incident_status,
    delete_incident
)
from app.data.datasets import load_all_csv_data
st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

# Ensure state keys exist (in case user opens this page first)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# Guard: if not logged in, send user back
if not st.session_state.logged_in:
    st.error("You must be logged in to view the dashboard.")
    if st.button("Go to login page"):
        st.switch_page("Home.py")   # back to the first page
    st.stop()

# If logged in, show dashboard content
st.title("📊 Dashboard")
st.success(f"Hello, **{st.session_state.username}**! You are logged in.")
# -------------------------------------
# DOMAIN SELECTOR
# -------------------------------------
domain = st.selectbox(
    "Choose a domain:",
    ["Cybersecurity", "Data Science", "IT Tickets"]
)

st.divider()
if domain == "Cybersecurity":
    st.title("Cyber Incidents Dashboard")

    conn = connect_database('DATA/intelligence_platform.db')

    incidents = get_all_incidents(conn)
    st.dataframe(incidents, use_container_width=True)

    with st.form("new_incident"):
        title = st.text_input("Incident Title")
        severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
        status = st.selectbox("Status", ["Open", "In Progress", "Resolved"])
        submitted = st.form_submit_button("Add Incident")

    if submitted and title:
        insert_incident(conn, title, severity, status)
        st.success("Incident added successfully!")
        st.rerun()

# --------------------------------------
# DATA SCIENCE DASHBOARD
# --------------------------------------
if domain == "Data Science":
    st.title("📈 Data Science Dashboard")

    # Simple example chart
    import pandas as pd

    history = pd.DataFrame({
        "epoch": [1, 2, 3, 4, 5],
        "accuracy": [0.70, 0.75, 0.82, 0.88, 0.91],
        "loss": [0.45, 0.33, 0.28, 0.22, 0.19]
    })

    st.subheader("Model Performance")
    st.line_chart(history, x="epoch", y=["accuracy", "loss"])
# --------------------------------------
# IT TICKETS DASHBOARD
# --------------------------------------
if domain == "IT Tickets":
    st.title("💼 IT Tickets Dashboard")

    st.info("IT Ticket dashboard coming soon!")

# Logout button
st.divider()
if st.button("Log out"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.info("You have been logged out.")
    st.switch_page("Home.py")
