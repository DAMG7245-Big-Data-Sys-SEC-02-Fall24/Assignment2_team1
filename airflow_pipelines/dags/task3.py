import os
from google.cloud import storage

# Set the path to your service account key file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/opt/airflow/config/gcp.json"

def upload_folder_to_bucket(bucket_name, source_folder_path, destination_blob_name):
    # Initialize a storage client
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)

    # Walk through the source folder
    for root, dirs, files in os.walk(source_folder_path):
        for file in files:
            local_file_path = os.path.join(root, file)
            relative_path = os.path.relpath(local_file_path, source_folder_path)
            blob_path = os.path.join(destination_blob_name, relative_path)

            # Upload the file to GCP bucket
            blob = bucket.blob(blob_path)
            blob.upload_from_filename(local_file_path)
            print(f"File {local_file_path} uploaded to {blob_path}.")

def run_upload_task():
    # Define the bucket name and folder paths
    bucket_name = "assignment2-damg7245-t1"  # Your GCP bucket
    source_folder_path = '/opt/airflow/dags/data/extracted_pdfs'  # Folder containing extracted PDFs
    destination_blob_name = "gaia_extracted_pdfs"  # Destination path in GCP bucket

    # Call the function to upload PDFs to the GCP bucket
    upload_folder_to_bucket(bucket_name, source_folder_path, destination_blob_name)
