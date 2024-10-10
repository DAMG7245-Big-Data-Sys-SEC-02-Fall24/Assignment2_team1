import streamlit as st
import os
import sys

# Add the 'pages' directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'pages')))
from utils import authenticate_user, register_user, logout_user, refresh_access_token

# Session defaults
session_defaults = {
    'is_authenticated': False,
    'access_token': None,
    'refresh_token': None,
    'display_login': True,
    'display_register': False,
    'user_email': None,
    'current_page': 'Home',
    'pages': ['Home', 'Summary', 'Querying']
}

def initialize_session_state():
    for key, default in session_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default

def clear_session_state():
    for key in session_defaults.keys():
        st.session_state[key] = session_defaults[key]

def main():
    initialize_session_state()
    set_page_config()
    if not st.session_state['is_authenticated']:
        login_page()
    else:
        display_sidebar()
        display_page_content()

def set_page_config():
    st.set_page_config(
        page_title="Assignment 2 Application",
        page_icon="🌐",
        initial_sidebar_state='expanded'
    )

def login_page():
    st.title("Welcome to the Application")
    if st.session_state['display_login']:
        display_login_form()
    elif st.session_state['display_register']:
        display_register_form()

def display_login_form():
    st.subheader("Login")
    with st.form("login_form"):
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        submit = st.form_submit_button("Login")

    if submit:
        process_login(email, password)

    st.write("Don't have an account?")
    st.button("Register", on_click=show_register_form)

def display_register_form():
    st.subheader("Register")
    with st.form("register_form"):
        username = st.text_input("Username", key="register_username")
        email = st.text_input("Email", key="register_email")
        password = st.text_input("Password", type="password", key="register_password")
        submit = st.form_submit_button("Register")

    if submit:
        process_registration(username, email, password)

    st.write("Already have an account?")
    st.button("Back to Login", on_click=show_login_form)

def show_register_form():
    st.session_state['display_login'] = False
    st.session_state['display_register'] = True
    st.rerun()

def show_login_form():
    st.session_state['display_login'] = True
    st.session_state['display_register'] = False
    st.rerun()

def process_login(email, password):
    if email and password:
        with st.spinner("Authenticating..."):
            success, error_message = authenticate_user(email, password)
        if success:
            st.success("Login successful!")
            st.session_state['is_authenticated'] = True
            st.session_state['user_email'] = email
            st.session_state['display_login'] = False
            st.rerun()
        else:
            st.error(error_message)
    else:
        st.warning("Please enter both email and password.")


def process_registration(username, email, password):
    if username and email and password:
        with st.spinner("Registering..."):
            success, error_message = register_user(username, email, password)
        if success:
            st.success("Registration successful! Please log in.")
            st.session_state['display_register'] = False
            st.session_state['display_login'] = True
            st.rerun()
        else:
            st.error(error_message)
    else:
        st.warning("Please fill all fields.")

def display_sidebar():
    st.sidebar.title("Navigation")
    st.sidebar.write(f"Logged in as: {st.session_state['user_email']}")
    page = st.sidebar.radio("Go to", st.session_state['pages'], index=st.session_state['pages'].index(st.session_state['current_page']))
    st.session_state['current_page'] = page
    st.sidebar.button("Logout", on_click=process_logout)

def display_page_content():
    if st.session_state['current_page'] == "Home":
        from pages import home
        home.display()
    elif st.session_state['current_page'] == "Summary":
        from pages import summary
        summary.display()
    elif st.session_state['current_page'] == "Querying":
        from pages import querying
        querying.display()

def process_logout():
    logout_user()
    st.success("Logged out successfully.")
    st.rerun()

if __name__ == "__main__":
    main()
