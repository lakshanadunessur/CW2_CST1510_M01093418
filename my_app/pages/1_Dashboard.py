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
from app.data.datasets import(
     get_all_datasets,
     insert_datasets,
     update_dataset_name,
     delete_dataset
)

from app.data.schema import load_all_csv_data
conn = connect_database('DATA/intelligence_platform.db')

df_incidents = get_all_incidents(conn)
df_datasets = get_all_datasets(conn)
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
st.title("Welcome to Dashboard!!")
st.success(f"Hello, **{st.session_state.username}**! You are logged in.")
# -------------------------------------
# DOMAIN SELECTOR
# -------------------------------------
domain = st.selectbox(
    "Choose a domain:",
    ["Cybersecurity", "Data Science", "IT Tickets"]
)

st.divider()
#Cybersecurity domain
if domain == "Cybersecurity":

        st.header("🛡 Cybersecurity Analytics")

        incidents = get_all_incidents(conn)

        if incidents.empty:
            st.warning("No incident data found.")
        else:
            # Metrics Row
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Incidents", len(incidents))
            with col2:
                high_count = len(incidents[incidents["severity"] == "High"])
                st.metric("High Severity", high_count)
            with col3:
                critical_count = len(incidents[incidents["severity"] == "Critical"])
                st.metric("Critical Incidents", critical_count)

            st.divider()

        st.title("Cyber Incidents Dashboard")
        conn = connect_database('DATA/intelligence_platform.db')
        incidents = get_all_incidents(conn)
        st.dataframe(incidents, use_container_width=True)

        # ------------------------ NEW LAYOUT FOR CHARTS ------------------------
        # Bar charts side by side
        st.subheader(" Overview Charts")

        colA, colB = st.columns(2)

        with colA:
            st.markdown("### Incidents by Category")
            if not incidents.empty:
                cat_counts = incidents.groupby("category").size().reset_index(name="count")
                st.bar_chart(cat_counts, x="category", y="count", use_container_width=True)
            else:
                st.info("No data available to plot.")

        with colB:
            st.markdown("### Incidents by Severity")
            if not incidents.empty:
                sev_counts = incidents.groupby("severity").size().reset_index(name="count")
                st.bar_chart(sev_counts, x="severity", y="count", use_container_width=True)
            else:
                st.info("No data available.")

        st.divider()

        # --------------------- PLOTLY LINE CHART ---------------------
        st.subheader(" Incidents Over Time (Plotly)")

        if not incidents.empty:
            import plotly.express as px

            incidents["timestamp"] = pd.to_datetime(incidents["timestamp"], errors="coerce")
            time_data = incidents.groupby("timestamp").size().reset_index(name="count")
            fig_line = px.line(time_data, x="timestamp", y="count", title="Incident Trend Over Time")
            st.plotly_chart(fig_line, use_container_width=True)
        else:
            st.info("No time-based data available.")

        # --------------------- PLOTLY PIE CHART ---------------------
        st.subheader(" Category Distribution (Pie Chart)")

        if not incidents.empty:
            fig_pie = px.pie(cat_counts, names="category", values="count", title="Incidents by Category")
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No data to generate pie chart.")

        st.divider()

        # --------------------- FORM SECTION ---------------------
        with st.form("new_incident"):
            title = st.text_input("Incident Title")
            severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
            status = st.selectbox("Status", ["Open", "In Progress", "Resolved"])
            submitted = st.form_submit_button("Add Incident")

        if submitted and title:
            insert_incident(conn, title, severity, status)
            st.success("Incident added successfully!")
            st.rerun()
st.divider()
# ---------------------------------------------------
# DATA SCIENCE DASHBOARD
# ---------------------------------------------------

if domain == "Data Science":

    st.header("📊 Data Science Analytics")

    datasets = get_all_datasets(conn)

    if datasets.empty:
        st.warning("No datasets data found.")
    else:
        # ---------------- METRICS ROW ----------------
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Total Datasets", len(datasets))

        with col2:
            avg_rows = int(datasets["rows"].mean())
            st.metric("Average Rows", avg_rows)

        with col3:
            avg_cols = int(datasets["columns"].mean())
            st.metric("Average Columns", avg_cols)

        st.divider()

        # ---------------- DATA TABLE ----------------
        st.title("Data Science Dashboard")
        st.dataframe(datasets, use_container_width=True)

        # ---------------- OVERVIEW CHARTS ----------------
        st.subheader(" Overview Charts")

        colA, colB = st.columns(2)

        # -------- DATASETS BY ROW SIZE --------
        with colA:
            st.markdown("### Datasets by Number of Rows")

            row_bins = [0, 1000, 10000, 100000, float("inf")]
            row_labels = ["Small", "Medium", "Large", "Very Large"]

            datasets["row_size"] = pd.cut(
                datasets["rows"],
                bins=row_bins,
                labels=row_labels
            )

            row_counts = datasets.groupby("row_size").size().reset_index(name="count")
            st.bar_chart(row_counts, x="row_size", y="count", use_container_width=True)

        # -------- DATASETS BY COLUMN SIZE --------
        with colB:
            st.markdown("### Datasets by Number of Columns")

            col_bins = [0, 5, 10, 20, float("inf")]
            col_labels = ["Few", "Moderate", "Many", "Very Many"]

            datasets["column_size"] = pd.cut(
                datasets["columns"],
                bins=col_bins,
                labels=col_labels
            )

            col_counts = datasets.groupby("column_size").size().reset_index(name="count")
            st.bar_chart(col_counts, x="column_size", y="count", use_container_width=True)

        st.divider()

        # ---------------- PLOTLY PIE CHART ----------------
        st.subheader(" Dataset Size Distribution (Pie Chart)")

        import plotly.express as px

        size_counts = datasets.groupby("row_size").size().reset_index(name="count")

        fig_pie = px.pie(
            size_counts,
            names="row_size",
            values="count",
            title="Datasets by Size (Number of Rows)"
        )

        st.plotly_chart(fig_pie, use_container_width=True)

        st.divider()

        # ---------------- FORM SECTION ----------------
        with st.form("new_dataset"):
            name = st.text_input("Dataset Name")
            rows = st.number_input("Number of Rows", min_value=1, step=1)
            columns = st.number_input("Number of Columns", min_value=1, step=1)
            submitted = st.form_submit_button("Add Dataset")

        if submitted and name:
            insert_datasets(conn, name, rows, columns)
            st.success("Dataset added successfully!")
            st.rerun()



# --------------------------------------
# IT TICKETS DASHBOARD
# --------------------------------------
if domain == "IT Tickets":
    st.title("💼 IT Tickets Dashboard")


# Logout button
st.divider()
if st.button("Log out"):
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.info("You have been logged out.")
    st.switch_page("Home.py")
