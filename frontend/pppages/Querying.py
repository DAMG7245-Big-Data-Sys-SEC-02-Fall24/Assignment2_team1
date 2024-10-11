import streamlit as st
import requests
from session_store import session_store
from authentication import auth
from utils import get_headers, API_BASE_URL


def display_query_page():
    """Main function to display the querying page."""
    st.title("Querying")
    st.write("This page allows you to perform queries.")

    # Ensure the user is authenticated before proceeding
    auth.check_access()

    query_text = st.text_input("Enter your query")

    # Submit query button
    if st.button("Submit Query"):
        if query_text:
            process_query(query_text)
        else:
            st.warning("Please enter a query.")


def process_query(query_text):
    """Process the query by sending a POST request to the API."""
    query_url = f"{API_BASE_URL}/query"

    with st.spinner("Processing query..."):
        try:
            response = requests.post(
                query_url,
                headers=get_headers(),
                json={"query": query_text}
            )

            # Handle potential unauthorized access (expired token)
            if response.status_code == 401:
                handle_unauthorized_access(query_url, query_text)
            elif response.status_code == 200:
                display_query_result(response)
            else:
                handle_query_error(response)

        except Exception as e:
            st.error(f"An error occurred: {e}")


def handle_unauthorized_access(query_url, query_text):
    """Handle unauthorized access by refreshing the token and retrying the query."""
    st.warning("Session expired. Attempting to refresh the token...")

    if auth.refresh_token():
        # Retry the request after refreshing the token
        response = requests.post(
            query_url,
            headers=get_headers(),
            json={"query": query_text}
        )
        if response.status_code == 200:
            display_query_result(response)
        else:
            st.error("Failed to process query after refreshing token.")
    else:
        st.error("Authentication failed. Please log in again.")
        session_store.clear_session()  # Clear session on failure
        st.rerun()  # Redirect to login


def display_query_result(response):
    """Display the result of the query if the response is successful."""
    data = response.json()
    st.success("Query processed successfully!")
    st.write(data.get("result", "No result available."))


def handle_query_error(response):
    """Handle errors when processing the query."""
    error_detail = response.json().get("detail", "Failed to process query.")
    st.error(error_detail)


# Call the display function to render the page
# display_query_page()
import streamlit as st
from google.cloud import storage
from google.auth.exceptions import DefaultCredentialsError

# Function to initialize GCP storage client
def get_gcp_storage_client():
    try:
        return storage.Client()  # Automatically picks up credentials from the environment
    except DefaultCredentialsError:
        st.error("Google Cloud credentials not found. Please configure your credentials.")
        return None

# Function to list files from a GCP bucket
def list_files_in_gcp(bucket_name):
    client = get_gcp_storage_client()
    if not client:
        return []

    try:
        bucket = client.get_bucket(bucket_name)
        blobs = bucket.list_blobs()  # List all files in the bucket
        return [blob.name for blob in blobs]
    except Exception as e:
        st.error(f"Error accessing bucket {bucket_name}: {e}")
        return []

# Function to display file picker with checkboxes and store selections in session state
def display_file_picker(bucket_name):
    st.title("GCP Object Store File Picker")

    # List files from GCP bucket
    files = list_files_in_gcp(bucket_name)

    if files:
        st.subheader(f"Files in {bucket_name}")

        # Create checkboxes for each file
        selected_files = []
        for file in files:
            if st.checkbox(file, key=file):
                selected_files.append(file)

        # Store selected files in session state
        st.session_state['selected_files'] = selected_files

        # Show selected files
        if selected_files:
            st.success(f"Selected files: {', '.join(selected_files)}")
        else:
            st.info("No files selected.")
    else:
        st.warning(f"No files found in the bucket {bucket_name}.")

# Example usage
bucket_name = "your-gcp-bucket-name"  # Replace with your GCP bucket name
display_file_picker(bucket_name)

# Display selected files (outside the picker function if needed)
if 'selected_files' in st.session_state and st.session_state['selected_files']:
    st.write("Files selected from session state:")
    st.write(st.session_state['selected_files'])
