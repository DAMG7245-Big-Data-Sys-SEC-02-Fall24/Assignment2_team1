import streamlit as st
import re
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL")

def validate_email(email):
    """Validate email format using regex."""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)

def validate_password(password):
    """Validate password with minimum 8 characters, at least one number, one uppercase, and one lowercase."""
    if len(password) < 8:
        return "Password must be at least 8 characters long."
    if not any(char.isdigit() for char in password):
        return "Password must contain at least one number."
    if not any(char.isupper() for char in password):
        return "Password must contain at least one uppercase letter."
    if not any(char.islower() for char in password):
        return "Password must contain at least one lowercase letter."
    return None

def register(username, email, password):
    data = {"Username": username, "Email": email, "Password": password}
    try:
        response = requests.post(f"{API_URL}/register", json=data)
        if response.status_code == 200:
            return {"success": True, "message": "Registration successful!"}
        else:
            return {"success": False, "message": response.json().get("detail", "Registration failed.")}
    except requests.exceptions.RequestException as e:
        return {"success": False, "message": f"Error: {str(e)}"}

def login(email, password):
    data = {"Email": email, "Password": password}
    try:
        response = requests.post(f"{API_URL}/login", json=data)
        if response.status_code == 200:
            return {"success": True, "token": response.json().get("access_token")}
        else:
            return {"success": False, "message": response.json().get("detail", "Login failed.")}
    except requests.exceptions.RequestException as e:
        return {"success": False, "message": f"Error: {str(e)}"}

def show_popup(message, success=True):
    if success:
        st.success(message)
    else:
        st.error(message)

def landing_page():
    st.title("Your Project Title")

    if "show_registration" not in st.session_state:
        st.session_state["show_registration"] = False

    if not st.session_state["show_registration"]:
        st.subheader("Login")

        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        login_button = st.button("Login")

        if login_button:
            if not email or not password:
                st.error("Email and Password cannot be empty!")
            elif not validate_email(email):
                st.error("Please enter a valid email address!")
            else:
                login_response = login(email, password)
                if login_response["success"]:
                    st.session_state["jwt_token"] = login_response.get("token")
                    st.success("Login successful!")
                    #st.session_state["login_email"] = ""
                    #st.session_state["login_password"] = ""
                else:
                    show_popup(login_response["message"], success=False)

        st.button("Don't have an account? Click here to Register", on_click=lambda: st.session_state.update({"show_registration": True}))

    if st.session_state["show_registration"]:
        st.subheader("Register")

        reg_username = st.text_input("Username", key="register_username")
        reg_email = st.text_input("Email", key="register_email")
        reg_password = st.text_input("Password", type="password", key="register_password")

        register_button = st.button("Register")
        if register_button:
            if not reg_username or not reg_email or not reg_password:
                st.error("Username, Email, and Password cannot be empty!")
            elif not validate_email(reg_email):
                st.error("Please enter a valid email address!")
            else:
                password_error = validate_password(reg_password)
                if password_error:
                    st.error(password_error)
                else:
                    register_response = register(reg_username, reg_email, reg_password)
                    if register_response["success"]:
                        show_popup(register_response["message"], success=True)
                        st.session_state["show_registration"] = False
                    else:
                        show_popup(register_response["message"], success=False)

        st.button("Back to Login", on_click=lambda: st.session_state.update({"show_registration": False}))
