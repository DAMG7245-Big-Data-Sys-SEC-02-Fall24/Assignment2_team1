import streamlit as st
from services.session_store import session_store
from services.authentication import auth
from services.ObjectStore import list_files_in_gcs  # Assuming you have a function to list GCS files
import os
from dotenv import load_dotenv
import requests
import logging

# Load environment variables
load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL")

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)

session_defaults = {
    'display_login': True,
    'display_register': False,
    'selected_file': "Select a PDF document",
    'model_type': "Open Source Extractor",
    'operation': "Summarize",
    'gpt_model': "gpt-4o-mini",
    'query_text': None
}


def initialize_session_state():
    for key, default in session_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default


def clear_session_storage():
    print("Clearing storage")
    for key, default in session_defaults.items():
        if key != "selected_llm":
            st.session_state[key] = default


def main():
    # Set Streamlit page configuration
    logging.info("Setting Streamlit page configuration")
    initialize_session_state()

    # Authentication handling
    if not session_store.is_authenticated():
        logging.info("User not authenticated, showing login page")
        login_page()
    else:
        logging.info("User authenticated, displaying sidebar and main content")
        set_page_config()
        display_sidebar()  # Display the file picker in the sidebar
        display_page_content()  # Main content

def set_page_config():
    try:
        st.set_page_config(
            page_title="Assignment 2 Application",
            page_icon="🌐",
            layout="wide",
            initial_sidebar_state='expanded'
        )
        logging.info("Page configuration set successfully")
    except Exception as e:
        logging.error(f"Error setting page config: {e}")

def login_page():
    st.set_page_config(layout="centered")

    st.markdown(
        """
        <style>
        .container {
            text-align: center;            
            font-family: Arial, sans-serif;
        }
        .title {
            font-size: 2.5em;
            color: #2E86C1;
            margin-bottom: 10px;
        }
        .welcome {
            font-size: 1.2em;
            color: #555;
            margin-bottom: 20px;
        }
        .features {
            background-color: #f5f5f5;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .features h3 {
            color: #1A5276;
        }
        .features ul {
            text-align: center;
            list-style-type: none;
            padding-left: 0;
        }
        .features ul li {
            font-size: 1.1em;
            color: #333;
            margin-bottom: 10px;
            padding-left: 1.5em;
            text-indent: -1.5em;
        }
        .features ul li:before {
            content: '✓';
            margin-right: 10px;
            color: #1ABC9C;
        }
        .footer {
            margin-top: 30px;
            font-size: 0.9em;
            color: #777;
        }
        </style>
        <div class="container">
            <div class="title">Document Query Platform</div>            
            <div class="features">
                <h3>Features available:</h3>
                <ul>
                    <li>Secure Document Summarization and Querying</li>
                    <li>Access to Multiple Document Extractors (Open Source & Enterprise)</li>
                    <li>Seamless Integration with GPT Models for Text Extraction</li>
                    <li>View and Interact with Pre-Processed Documents</li>
                </ul>
            </div>            
        </div>
        """,
        unsafe_allow_html=True
    )

    if session_store.get_value('display_login'):
        display_login_form()
    elif session_store.get_value('display_register'):
        display_register_form()

def display_pdf():
    from streamlit_pdf_viewer import pdf_viewer
    from services.ObjectStore import download_file_from_gcs
    bucket_name = "assignment2-damg7245-t1"
    filePath = download_file_from_gcs(bucket_name, st.session_state['selected_file'])
    pdf_viewer(filePath)

def display_login_form():
    st.subheader("Login")
    logging.info("Displaying login form")
    with st.form("login_form"):
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        submit = st.form_submit_button("Login")

    if submit:
        try:
            logging.info(f"Attempting login for user: {email}")
            auth.login(email, password)
        except Exception as e:
            logging.error(f"Login failed for user {email}: {e}")

    st.write("Don't have an account?")
    if st.button("Register"):
        show_register_form()

def display_register_form():
    st.subheader("Register")
    logging.info("Displaying register form")
    with st.form("register_form"):
        username = st.text_input("Username", key="register_username")
        email = st.text_input("Email", key="register_email")
        password = st.text_input("Password", type="password", key="register_password")
        submit = st.form_submit_button("Register")

    if submit:
        try:
            logging.info(f"Attempting registration for user: {email}")
            auth.register(username, email, password)
        except Exception as e:
            logging.error(f"Registration failed for user {email}: {e}")

    st.write("Already have an account?")
    st.button("Back to Login", on_click=show_login_form)

def show_register_form():
    logging.info("Switching to register form")
    session_store.set_value('display_login', False)
    session_store.set_value('display_register', True)
    st.rerun()

def show_login_form():
    logging.info("Switching to login form")
    session_store.set_value('display_login', True)
    session_store.set_value('display_register', False)
    st.rerun()

def display_sidebar():
    logging.info("Displaying sidebar content")
    st.sidebar.write(f"Logged in as: {session_store.get_user_email()}")
    if st.sidebar.button("Logout"):
        logging.info("Logging out user")
        auth.logout()
        st.stop()
    st.sidebar.title("File Explorer")
    bucket_name = "assignment2-damg7245-t1"  # Replace with your GCP bucket name
    prefix = "gaia_extracted_pdfs"  # Folder prefix

    try:
        logging.info(f"Fetching files from GCS bucket: {bucket_name} with prefix: {prefix}")
        files = list_files_in_gcs(bucket_name, prefix=prefix)

        if files:
            files.insert(0, "Select a PDF document")
            selected_file = st.sidebar.selectbox(
                "Select a PDF document",
                files,
                index=0,
                key="selected_file",
                on_change=on_file_change
            )
            logging.info(f"Selected file: {selected_file}")

            st.sidebar.selectbox(
                "Choose Extractor",
                ["Open Source Extractor", "Closed Source Extractor"],
                key="model_type",
                disabled=(selected_file == "Select a PDF document"),
            )

            st.sidebar.selectbox(
                "What would you like to do?",
                ["Summarize", "Query", "View"],
                key="operation",
                disabled=(selected_file == "Select a PDF document")
            )

            st.sidebar.selectbox(
                "Choose GPT Model",
                ["gpt-4o-mini", "gpt-4o"],
                key="gpt_model",
                disabled=(selected_file == "Select a PDF document")
            )

            if st.sidebar.button("Clear Selection", disabled=(selected_file == "Select a PDF document"), on_click=reset_selected_file):
                logging.info("Clearing file selection")
                # reset_selected_file()
                st.rerun()

        else:
            st.sidebar.warning(f"No files found in the bucket {bucket_name} with prefix {prefix}.")
            logging.warning(f"No files found in the bucket {bucket_name} with prefix {prefix}")

    except Exception as e:
        st.sidebar.error(f"Error occurred: {e}")
        logging.error(f"Error fetching files from GCS: {e}")

def on_file_change():
    logging.info("File selection changed, resetting form values")
    st.session_state['model_type'] = "Open Source Extractor"
    st.session_state['operation'] = "View"
    st.session_state['gpt_model'] = "gpt-4o-mini"
    st.session_state['query_text'] = None

def reset_selected_file():
    logging.info("Resetting selected file and form values")
    st.session_state['model_type'] = "Open Source Extractor"
    st.session_state['operation'] = "View"
    st.session_state['query_text'] = None
    st.session_state['gpt_model'] = "gpt-4o-mini"
    st.session_state['selected_file'] = "Select a PDF document"

def display_page_content():
    selected_file = st.session_state.get('selected_file')
    if selected_file and selected_file != "Select a PDF document":
        st.subheader(f"Processing: {selected_file}")
        logging.info(f"Processing file: {selected_file}")

        if st.session_state['operation'] == "Summarize":
            if st.button("Summarize Document", type="primary"):
                logging.info(f"Summarizing document: {selected_file}")
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
                        logging.error(f"Error summarizing document: {error}")
                    else:
                        logging.info(summary)
                        # in summary replace ``` with """
                        try:
                            p = summary.replace("```", '"""')
                            p = p.replace("\"\"\"markdown", "")
                            st.markdown(p, unsafe_allow_html=True)
                            logging.info("Summary successfully displayed")
                        except Exception as e:
                            logging.error(f"Error displaying summary: {e}")
                            st.markdown(summary, unsafe_allow_html=True)


        elif st.session_state['operation'] == "Query":
            query_text = st.text_input("Enter your query:")

            if st.button("Submit Query"):
                if query_text:
                    logging.info(f"Submitting query: {query_text} for document: {selected_file}")
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
                            logging.error(f"Error querying document: {error}")
                        else:
                            st.write(f"Response: {response}")
                            try:
                                p = response.replace("```", '"""')
                                p = p.replace("\"\"\"markdown", "")
                                st.markdown(p, unsafe_allow_html=True)
                                logging.info("Summary successfully displayed")
                            except Exception as e:
                                logging.error(f"Error displaying summary: {e}")
                                st.markdown(response, unsafe_allow_html=True)


        elif (st.session_state['operation'] == "View"):
            display_pdf()

def process_document_name(document_name):
    return document_name.split("/")[-1].split(".")[0]

def summarize_document_api(document_name, model_type, gpt_model, access_token):
    summarize_url = f"{API_BASE_URL}/documents/summarize"
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        logging.info(f"Sending summarize request for document: {document_name}")
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
            logging.info(f"Summarize API call successful for document: {document_name}")
            return data.get("summary"), None
        else:
            logging.error(f"Summarize API failed with status code: {response.status_code}")
            return None, response.text
    except Exception as e:
        logging.error(f"Error during summarize API call: {e}")
        return None, f"An error occurred: {e}"

def query_document_api(document_name, query_text, model_type, gpt_model, access_token):
    query_url = f"{API_BASE_URL}/documents/query"
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        logging.info(f"Sending query request for document: {document_name} with query: {query_text}")
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
            logging.info(f"Query API call successful for document: {document_name}")
            return data.get("response"), None
        else:
            logging.error(f"Query API failed with status code: {response.status_code}")
            return None, response.text
    except Exception as e:
        logging.error(f"Error during query API call: {e}")
        return None, f"An error occurred: {e}"

if __name__ == "__main__":
    main()
