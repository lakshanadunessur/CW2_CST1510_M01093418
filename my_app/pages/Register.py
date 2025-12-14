import streamlit as st
import bcrypt
import os

USER_FILE = "DATA/user.txt"

#Function save user
def save_user(username, password):
    """Save a new user to user.txt with hashed password."""
    hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    with open(USER_FILE, "a") as f:
        f.write(f"{username},{hashed_pw}\n")
# Function load users
def load_users():
    users = {}
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            for line in f:
                uname, hpw = line.strip().split(",")
                users[uname] = hpw
    return users

st.title("Register New Account")

users = load_users()

new_username = st.text_input("Create Username")
new_password = st.text_input("Create Password", type="password")
confirm_password = st.text_input("Confirm Password", type="password")

#Creating a register button
if st.button("Register"):
    if new_username in users:
        st.error("Username already exists.")
    elif new_password != confirm_password:
        st.error("Passwords do not match.")
    elif len(new_password) < 3:
        st.error("Password must be at least 3 characters.")
    else:
        save_user(new_username, new_password)
        st.success("Account created successfully! You can now log in.")
        st.switch_page("Home.py")
