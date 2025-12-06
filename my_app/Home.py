import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import streamlit as st
import bcrypt
import os

USER_FILE = "DATA/user.txt"

def load_users():
    users = {}
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            for line in f:
                username, hashed_pw = line.strip().split(",")
                users[username] = hashed_pw
    return users

def verify_password(input_password, stored_hash):
    return bcrypt.checkpw(input_password.encode("utf-8"), stored_hash.encode("utf-8"))

# ---------------------------------------------------

st.title("Multi-Domain Intelligence Platform")

# Load existing users from user.txt
users = load_users()

# -----------------------------------------------
# Session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
# -----------------------------------------------

# If already logged in
if st.session_state.logged_in:
    st.success(f"Logged in as {st.session_state.username}")

    if st.button("Go to Dashboard"):
        st.switch_page("pages/1_Dashboard.py")

    if st.button("Log out"):
        st.session_state.logged_in = False

    st.stop()

# -----------------------------------------------
# LOGIN FORM
# -----------------------------------------------
username = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Login"):
    if username in users:
        stored_hash = users[username]
        if verify_password(password, stored_hash):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Login successful!")
            st.switch_page("pages/1_Dashboard.py")
        else:
            st.error("Incorrect password.")
    else:
        st.error("User does not exist.")