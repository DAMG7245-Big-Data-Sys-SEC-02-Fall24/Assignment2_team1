from google.cloud import storage
from google.oauth2 import service_account
import tempfile
from google.api_core.exceptions import Forbidden
import os
from dotenv import load_dotenv
load_dotenv()

# Function to initialize GCS client using service account credentials
def get_gcs_client():
    try:
        gcp_service_account = os.getenv("GCP_JSON")
        credentials = service_account.Credentials.from_service_account_file(gcp_service_account)
        client = storage.Client(credentials=credentials)
        return client
    except Exception as e:
        raise RuntimeError(f"Error initializing GCS client: {e}")

# Function to list files in a GCS bucket
def list_files_in_gcs(bucket_name, prefix=""):
    client = get_gcs_client()
    try:
        bucket = client.bucket(bucket_name)
        blobs = bucket.list_blobs(prefix=prefix)  # List files with a specific prefix (folder)
        result = []
        for blob in blobs:
            result.append(blob.name)
        return result
    except Forbidden as e:
        raise PermissionError(f"Permission denied: {e}")
    except Exception as e:
        raise RuntimeError(f"An error occurred while listing files: {e}")

# Function to download a file from GCS
def download_file_from_gcs(bucket_name, file_name):
    client = get_gcs_client()

    try:
        # Get the bucket and blob
        bucket = client.bucket(bucket_name)
        blob = bucket.blob(file_name)

        # Create a temporary directory
        temp_dir = tempfile.mkdtemp()

        # Define the local file path
        local_file_path = os.path.join(temp_dir, os.path.basename(file_name))

        # Download the file
        blob.download_to_filename(local_file_path)
        return local_file_path

    except Forbidden as e:
        raise PermissionError(f"Permission denied: {e}. Please check the service account permissions.")
    except Exception as e:
        raise RuntimeError(f"An error occurred: {e}")

if __name__ == "__main__":
    bucket_name = "assignment2-damg7245-t1"  # Replace with your GCP bucket name
    prefix = "gaia_extracted_pdfs"  # Folder prefix

    try:
        files = list_files_in_gcs(bucket_name, prefix=prefix)
        if files:
            print(f"Files in bucket {bucket_name}:")
            for file in files:
                print(file)
        else:
            print(f"No files found in the bucket {bucket_name}.")
    except PermissionError as e:
        print(f"Permission error: {e}")
    except RuntimeError as e:
        print(f"Runtime error: {e}")