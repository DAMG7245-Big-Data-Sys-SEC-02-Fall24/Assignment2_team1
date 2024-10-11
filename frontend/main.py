import streamlit as st
from session_store import session_store
from authentication import auth


def main():
    # Initialize session and authentication (instances already globally available)

    # Set Streamlit page configuration
    set_page_config()

    if not session_store.is_authenticated():
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
    if session_store.get_value('display_login'):
        display_login_form()
    elif session_store.get_value('display_register'):
        display_register_form()


def display_login_form():
    st.subheader("Login")
    with st.form("login_form"):
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        submit = st.form_submit_button("Login")

    if submit:
        auth.login(email, password)

    st.write("Don't have an account?")
    if st.button("Register"):
        show_register_form()


def display_register_form():
    st.subheader("Register")
    with st.form("register_form"):
        username = st.text_input("Username", key="register_username")
        email = st.text_input("Email", key="register_email")
        password = st.text_input("Password", type="password", key="register_password")
        submit = st.form_submit_button("Register")

    if submit:
        auth.register(username, email, password)

    st.write("Already have an account?")
    st.button("Back to Login", on_click=show_login_form)


def show_register_form():
    session_store.set_value('display_login', False)
    session_store.set_value('display_register', True)
    st.rerun()


def show_login_form():
    session_store.set_value('display_login', True)
    session_store.set_value('display_register', False)
    st.rerun()


def display_sidebar():
    st.sidebar.write(f"Logged in as: {session_store.get_user_email()}")
    st.sidebar.button("Logout", on_click=auth.logout)


def display_page_content():
    current_page = session_store.get_current_page()

if __name__ == "__main__":
    main()
