import streamlit as st
from ObjectStore import list_files_in_gcs  # Assuming you have a function to list GCS files
import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL")
st.set_page_config(page_title="GCS Document Processor", layout="wide")
# API call for summarizing the document
def summarize_document_api(document_name, model_type, gpt_model, access_token):
    summarize_url = f"{API_BASE_URL}/documents/summarize"
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        response = requests.post(
            summarize_url,
            json={
                "document_name": document_name,
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


# API call for querying the document
def query_document_api(document_name, query_text, model_type, gpt_model, access_token):
    query_url = f"{API_BASE_URL}/documents/query"
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        response = requests.post(
            query_url,
            json={
                "document_name": document_name,
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


# Function to reset selected file and clear session state
def reset_selected_file():
    st.session_state['model_type'] = "Open Source Extractor"
    st.session_state['operation'] = "Summarize"
    st.session_state['query_text'] = None
    st.session_state['gpt_model'] = "gpt-4o-mini"
    st.session_state['selected_file'] = "Select a PDF document"  # Set back to default option


# Callback function to reset the operation and model_type when the file changes
def on_file_change():
    st.session_state['model_type'] = "Open Source Extractor"
    st.session_state['operation'] = "Summarize"
    st.session_state['gpt_model'] = "gpt-4o-mini"
    st.session_state['query_text'] = None


# Function to display the dropdown for file selection and manage the document processing logic
def display_file_picker(bucket_name, prefix):
    st.title("File Explorer")

    # Create two columns
    col1, col2 = st.columns([1, 3])  # Left column for controls, right for results

    with col1:
        st.subheader("Document Selection and Processing")

        try:
            # Fetch files from GCS bucket
            files = list_files_in_gcs(bucket_name, prefix=prefix)

            if files:
                # Insert a default option for no file selected
                files.insert(0, "Select a PDF document")

                # Dropdown for selecting a document (default is "Select a PDF document")
                selected_file = st.selectbox(
                    "Select a PDF document",
                    files,
                    index=0,
                    key="selected_file",
                    on_change=on_file_change  # Trigger the on_file_change callback when the file selection changes
                )

                # Disable other controls if no file is selected
                is_file_selected = selected_file != "Select a PDF document"

                # Dropdown for choosing between Open Source Extractor or Closed Source Extractor
                st.selectbox(
                    "Choose Extractor",
                    ["Open Source Extractor", "Closed Source Extractor"],
                    key="model_type",
                    disabled=not is_file_selected,
                )

                # Choose operation: Summarize or Query
                st.selectbox(
                    "What would you like to do?",
                    ["Summarize", "Query", "View"],
                    key="operation",
                    disabled=not is_file_selected
                )

                # Choose GPT Model
                st.selectbox(
                    "Choose GPT Model",
                    ["gpt-4o-mini", "gpt-4o"],
                    key="gpt_model",
                    disabled=not is_file_selected
                )

                # Clear selection button (only enabled if a file is selected)
                if st.button("Clear Selection", disabled=not is_file_selected, on_click=reset_selected_file):
                    st.rerun()  # Rerun the app to reset everything

            else:
                st.warning(f"No files found in the bucket {bucket_name} with prefix {prefix}.")

        except Exception as e:
            st.error(f"Error occurred: {e}")

    with col2:
        # Display output based on selected operation (Summarize or Query)
        if 'selected_file' in st.session_state and st.session_state['selected_file'] != "Select a PDF document":
            st.subheader(f"Processing: {st.session_state['selected_file']}")

            # If the user selected Summarize
            if st.session_state['operation'] == "Summarize":
                with st.container():  # Using a container to box the summary
                    if st.button("Summarize Document"):
                        access_token = st.session_state.get('access_token')
                        print(access_token)
                        if access_token:
                            summary, error = summarize_document_api(
                                document_name=st.session_state['selected_file'],
                                model_type=st.session_state['model_type'],
                                gpt_model=st.session_state['gpt_model'],
                                access_token=access_token
                            )
                            if error:
                                st.error(f"Error: {error}")
                            else:
                                st.text_area("Summary:", summary, height=150)

            # If the user selected Query
            elif st.session_state['operation'] == "Query":
                query_text = st.text_input("Enter your query:")

                if st.button("Submit Query"):
                    if query_text:
                        access_token = st.session_state.get('access_token')
                        if access_token:
                            response, error = query_document_api(
                                document_name=st.session_state['selected_file'],
                                query_text=query_text,
                                model_type=st.session_state['model_type'],
                                gpt_model=st.session_state['gpt_model'],
                                access_token=access_token
                            )
                            if error:
                                st.error(f"Error: {error}")
                            else:
                                st.write(f"Response: {response}")

                        # After query is submitted, clear the input box
                        st.session_state.query_text = ""

            # If the user selected View
            if st.session_state['operation'] == "View":
                st.write("View:")
                with st.container():  # Similar to Summarize, just reuse the same dummy text area
                    st.text_area("View Document:", "This is a view-only version of the document.", height=150)


# Example usage in Streamlit
bucket_name = "assignment2-damg7245-t1"  # Replace with your GCP bucket name
prefix = "gaia_extracted_pdfs"  # Folder prefix

# Display the file picker and document processing interface
display_file_picker(bucket_name, prefix)
