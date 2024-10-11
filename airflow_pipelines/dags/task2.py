import os
import shutil
import zipfile

def extract_pdfs(source_dir, destination_dir, temp_dir='/tmp/gaia-temp'):
    # Create destination and temporary directories if they don't exist
    os.makedirs(destination_dir, exist_ok=True)
    os.makedirs(temp_dir, exist_ok=True)

    # Walk through the source directory and its subdirectories
    for root, _, files in os.walk(source_dir):
        for filename in files:
            file_path = os.path.join(root, filename)

            # Handle zip files
            if filename.lower().endswith('.zip'):
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(temp_dir)
                # Now search for PDFs in the extracted zip
                for root_zip, _, zip_files in os.walk(temp_dir):
                    for zip_filename in zip_files:
                        if zip_filename.lower().endswith('.pdf'):
                            zip_file_path = os.path.join(root_zip, zip_filename)
                            destination_file_path = os.path.join(destination_dir, zip_filename)
                            if not os.path.exists(destination_file_path):
                                shutil.copy(zip_file_path, destination_dir)
                                print(f'Copied from zip: {zip_file_path} to {destination_dir}')
                            else:
                                print(f'Skipped (already exists): {zip_filename}')
            
            # Handle regular PDFs
            elif filename.lower().endswith('.pdf'):
                destination_file_path = os.path.join(destination_dir, filename)
                if not os.path.exists(destination_file_path):
                    shutil.copy(file_path, destination_dir)
                    print(f'Copied: {file_path} to {destination_dir}')
                else:
                    print(f'Skipped (already exists): {filename}')
    
    # Clean up temp directory
    shutil.rmtree(temp_dir)

def run_extraction_task():
    # Define the source and destination directories
    source_directory = '/opt/airflow/dags/data/GAIA-dataset/'
    destination_directory = '/opt/airflow/dags/data/extracted_pdfs'
    
    # Run the PDF extraction
    extract_pdfs(source_directory, destination_directory)
