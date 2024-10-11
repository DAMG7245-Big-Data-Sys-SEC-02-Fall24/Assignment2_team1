import os
import pymupdf 
import csv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from google.cloud import storage
from dotenv import load_dotenv
import time
import tempfile

# Load environment variables
load_dotenv()

# MongoDB URI and GCP settings

mongo_uri = os.getenv('MONGO_URI')
gcp_bucket_name = "assignment2-damg7245-t1"

def connect_mongo():
    try:
        client = MongoClient(mongo_uri)
        client.admin.command('ping')
        print("MongoDB connection successful.")
        return client
    except ConnectionFailure as e:
        print(f"Could not connect to MongoDB: {e}")
        return None

def extract_tables(page):
    tables = []
    for table in page.find_tables():
        tables.append(table.extract())
    return tables

def save_table_to_gcs(table, bucket, gcs_path):
    with tempfile.NamedTemporaryFile(mode='w', newline='', delete=False) as temp_file:
        writer = csv.writer(temp_file)
        writer.writerows(table)
    
    temp_file_name = temp_file.name
    blob = bucket.blob(gcs_path)
    blob.upload_from_filename(temp_file_name)
    os.unlink(temp_file_name)
    return f"gs://{bucket.name}/{gcs_path}"

def extract_data_from_pdf(pdf_path, mongo_collection, storage_client):
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
    
    # Check if the PDF data already exists in the MongoDB collection
    if mongo_collection.find_one({"pdf_name": pdf_name}):
        print(f"PDF {pdf_name} already processed. Skipping...")
        return  # Skip processing if PDF data is already in the database
    
    bucket = storage_client.bucket(gcp_bucket_name)
    
    # Using pymupdf to open and process the PDF
    doc = pymupdf.open(pdf_path)
    all_pages_data = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text()

        # Extract tables
        tables = extract_tables(page)
        table_urls = []
        if tables:  # Only upload if tables exist
            for i, table in enumerate(tables):
                gcs_path = f"extracted_by_opensource_pdf/{pdf_name}/tables/table_page_{page_num + 1}_{i + 1}.csv"
                table_url = save_table_to_gcs(table, bucket, gcs_path)
                table_urls.append(table_url)

        # Extract images
        image_urls = []
        images = page.get_images(full=True)
        if images:  # Only upload if images exist
            for img_index, img in enumerate(images):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                
                gcs_path = f"extracted_by_opensource_pdf/{pdf_name}/images/image_page_{page_num + 1}_{img_index + 1}.{image_ext}"
                blob = bucket.blob(gcs_path)
                blob.upload_from_string(image_bytes, content_type=f"image/{image_ext}")
                image_url = f"gs://{bucket.name}/{gcs_path}"
                image_urls.append(image_url)

        page_data = {
            "page_number": page_num + 1,
            "text": text,
            "images": image_urls,
            "tables": table_urls
        }
        all_pages_data.append(page_data)

    pdf_data = {
        "pdf_name": pdf_name,
        "pages": all_pages_data
    }

    # Insert into MongoDB after processing
    mongo_collection.insert_one(pdf_data)
    print(f"Inserted {pdf_name} into MongoDB")
    doc.close()

def process_pdfs_in_folder(pdf_folder, mongo_collection, storage_client):
    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, filename)
            print(f"Processing {filename}...")
            extract_data_from_pdf(pdf_path, mongo_collection, storage_client)

def run_data_extraction_task():
    # MongoDB connection
    client = connect_mongo()
    if client:
        db = client["pdf_database_testing"]
        collection = db["pdf_collection_pymupdf"]

        # Local folder to store downloaded PDFs
        local_pdf_folder = "/opt/airflow/dags/data/extracted_pdfs"
        
        # Initialize GCP storage client
        storage_client = storage.Client()

        # Process the PDFs in the specified local folder
        process_pdfs_in_folder(local_pdf_folder, collection, storage_client)

if __name__ == "__main__":
    run_data_extraction_task()