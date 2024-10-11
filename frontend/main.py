import streamlit as st
from session_store import session_store
from authentication import auth
from ObjectStore import list_files_in_gcs  # Assuming you have a function to list GCS files
import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL")

def main():
    # Set Streamlit page configuration
    set_page_config()

    # Authentication handling
    if not session_store.is_authenticated():
        login_page()
    else:
        display_sidebar()  # Display the file picker in the sidebar
        display_page_content()  # Main content

def set_page_config():
    st.set_page_config(
        page_title="Assignment 2 Application",
        page_icon="🌐",
        layout="wide",
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

    st.sidebar.title("File Explorer")
    bucket_name = "assignment2-damg7245-t1"  # Replace with your GCP bucket name
    prefix = "gaia_extracted_pdfs"  # Folder prefix

    try:
        # Fetch files from GCS bucket
        files = list_files_in_gcs(bucket_name, prefix=prefix)

        if files:
            # Insert a default option for no file selected
            files.insert(0, "Select a PDF document")

            # Dropdown for selecting a document (default is "Select a PDF document")
            selected_file = st.sidebar.selectbox(
                "Select a PDF document",
                files,
                index=0,
                key="selected_file",
                on_change=on_file_change  # Trigger the on_file_change callback when the file selection changes
            )

            # Dropdown for choosing between Open Source Extractor or Closed Source Extractor
            st.sidebar.selectbox(
                "Choose Extractor",
                ["Open Source Extractor", "Closed Source Extractor"],
                key="model_type",
                disabled=(selected_file == "Select a PDF document"),
            )

            # Choose operation: Summarize or Query
            st.sidebar.selectbox(
                "What would you like to do?",
                ["Summarize", "Query", "View"],
                key="operation",
                disabled=(selected_file == "Select a PDF document")
            )

            # Choose GPT Model
            st.sidebar.selectbox(
                "Choose GPT Model",
                ["gpt-4o-mini", "gpt-4o"],
                key="gpt_model",
                disabled=(selected_file == "Select a PDF document")
            )

            # Clear selection button (only enabled if a file is selected)
            if st.sidebar.button("Clear Selection", disabled=(selected_file == "Select a PDF document")):
                reset_selected_file()
                st.rerun()  # Rerun the app to reset everything

        else:
            st.sidebar.warning(f"No files found in the bucket {bucket_name} with prefix {prefix}.")

    except Exception as e:
        st.sidebar.error(f"Error occurred: {e}")

def on_file_change():
    st.session_state['model_type'] = "Open Source Extractor"
    st.session_state['operation'] = "Summarize"
    st.session_state['gpt_model'] = "gpt-4o-mini"
    st.session_state['query_text'] = None

def reset_selected_file():
    st.session_state['model_type'] = "Open Source Extractor"
    st.session_state['operation'] = "Summarize"
    st.session_state['query_text'] = None
    st.session_state['gpt_model'] = "gpt-4o-mini"
    st.session_state['selected_file'] = "Select a PDF document"  # Set back to default option

def display_page_content():
    selected_file = st.session_state.get('selected_file')
    if selected_file and selected_file != "Select a PDF document":
        st.subheader(f"Processing: {selected_file}")

        if st.session_state['operation'] == "Summarize":
            if st.button("Summarize Document", type="primary"):
                access_token = st.session_state.get('access_token')
                if access_token:
                    summary, error = summarize_document_api(
                        document_name=selected_file,
                        model_type=st.session_state['model_type'],
                        gpt_model=st.session_state['gpt_model'],
                        access_token=access_token
                    )
                    if error:
                        st.error(f"Error: {error}")
                    else:
                        st.text_area("Summary:", summary, height=150)

        elif st.session_state['operation'] == "Query":
            query_text = st.text_input("Enter your query:")

            if st.button("Submit Query"):
                if query_text:
                    access_token = st.session_state.get('access_token')
                    if access_token:
                        response, error = query_document_api(
                            document_name=selected_file,
                            query_text=query_text,
                            model_type=st.session_state['model_type'],
                            gpt_model=st.session_state['gpt_model'],
                            access_token=access_token
                        )
                        if error:
                            st.error(f"Error: {error}")
                        else:
                            st.write(f"Response: {response}")

        elif st.session_state['operation'] == "View":
            st.write("View:")
            st.text_area("View Document:", "This is a view-only version of the document.", height=150)

def process_document_name(document_name):
    # pdf_name 'gaia_extracted_pdfs/021a5339-744f-42b7-bd9b-9368b3efda7a.pdf' -> '021a5339-744f-42b7-bd9b-9368b3efda7a'
    return document_name.split("/")[-1].split(".")[0]
def summarize_document_api(document_name, model_type, gpt_model, access_token):
    summarize_url = f"{API_BASE_URL}/documents/summarize"
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        response = requests.post(
            summarize_url,
            json={
                "document_name": process_document_name(document_name),
                "model_type": model_type,
                "gpt_model": gpt_model
            },
            headers=headers
        )
        if response.status_code == 200:
            data = response.json()
            return data.get("summary"), None
        else:
            return None, response.text
    except Exception as e:
        return None, f"An error occurred: {e}"

def query_document_api(document_name, query_text, model_type, gpt_model, access_token):
    query_url = f"{API_BASE_URL}/documents/query"
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        response = requests.post(
            query_url,
            json={
                "document_name": process_document_name(document_name),
                "query_text": query_text,
                "model_type": model_type,
                "gpt_model": gpt_model
            },
            headers=headers
        )
        if response.status_code == 200:
            data = response.json()
            return data.get("response"), None
        else:
            return None, response.text
    except Exception as e:
        return None, f"An error occurred: {e}"

if __name__ == "__main__":
    main()
    st.markdown(
        """
        <style>
            .stSidebar {
                width: 900px !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

