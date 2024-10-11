import os
import requests
import fitz
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from google.cloud import storage
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set API key for pdf.co
API_KEY = os.getenv('PDFCO_API_KEY')

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

def upload_file(pdf_path):
    url = "https://api.pdf.co/v1/file/upload"
    headers = {'x-api-key': API_KEY}
    files = {'file': open(pdf_path, 'rb')}
    response = requests.post(url, headers=headers, files=files)
    if response.status_code == 200:
        data = response.json()
        if not data['error']:
            return data['url']
        else:
            print(f"Error uploading file: {data['message']}")
            return None
    else:
        print(f"Error uploading file: {response.status_code} {response.reason}")
        return None

def get_pdf_info(pdf_url):
    url = "https://api.pdf.co/v1/pdf/info"
    headers = {'x-api-key': API_KEY}
    params = {'url': pdf_url}
    response = requests.post(url, headers=headers, data=params)
    if response.status_code == 200:
        data = response.json()
        if not data['error']:
            return data['info']
        else:
            print(f"Error getting PDF info: {data['message']}")
            return None
    else:
        print(f"Error getting PDF info: {response.status_code} {response.reason}")
        return None

def extract_text_from_pdf(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        extracted_text = {}
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            extracted_text[page_num + 1] = page.get_text("text")
        doc.close()
        return extracted_text
    except Exception as e:
        print(f"Error extracting text from {pdf_path}: {e}")
        return None

def extract_tables_from_pdf_url(pdf_url, pages):
    url = "https://api.pdf.co/v1/pdf/convert/to/csv"
    headers = {'x-api-key': API_KEY}
    params = {
        'url': pdf_url,
        'pages': pages,
        'inline': 'true',
        'isOCR': 'true',
        'ocrLanguages': 'eng',
        'unwrap': 'true',
    }
    response = requests.post(url, headers=headers, data=params)
    if response.status_code == 200:
        data = response.json()
        if not data['error']:
            csv_content = data['body']
            if csv_content.strip() and len(csv_content.split('\n')) > 1:
                return csv_content
            else:
                print(f"No tables found on page {pages}")
                return None
        else:
            return None
    else:
        return None

def save_to_gcs(bucket, content, gcs_path):
    blob = bucket.blob(gcs_path)
    blob.upload_from_string(content)
    return f"gs://{bucket.name}/{gcs_path}"

def extract_data_from_pdf(pdf_path, mongo_collection, storage_client):
    pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]

    # Check if the PDF already exists in MongoDB
    if mongo_collection.find_one({"pdf_name": pdf_name}):
        print(f"PDF {pdf_name} already exists in MongoDB. Skipping processing.")
        return

    # Upload the PDF and get its URL
    pdf_url = upload_file(pdf_path)
    if not pdf_url:
        print(f"Failed to upload PDF {pdf_path}")
        return

    # Get PDF info to get the number of pages
    pdf_info = get_pdf_info(pdf_url)
    if not pdf_info:
        print(f"Failed to get info for PDF {pdf_path}")
        return

    num_pages = int(pdf_info.get('PageCount', pdf_info.get('pageCount', 0)))
    if num_pages == 0:
        print(f"Could not determine the number of pages for {pdf_name}")
        return

    # Extract text from the PDF using fitz
    extracted_text = extract_text_from_pdf(pdf_path)
    if extracted_text:
        print(f"Extracted text for {pdf_name}.")
    else:
        print(f"No text found for {pdf_name}.")
        extracted_text = {}

    bucket = storage_client.bucket(gcp_bucket_name)
    all_pages_data = []

    for page_num in range(1, num_pages + 1):
        pages_str = str(page_num)
        print(f"Processing page {page_num} of {num_pages}...")

        # Extract tables using pdf.co
        table_csv = extract_tables_from_pdf_url(pdf_url, pages_str)
        table_urls = []
        if table_csv:
            gcs_path = f"extracted_by_pdfco/{pdf_name}/tables/table_page_{page_num}.csv"
            table_url = save_to_gcs(bucket, table_csv, gcs_path)
            table_urls.append(table_url)
            print(f"Extracted table for page {page_num}.")

        # Get text content
        text_content = extracted_text.get(page_num, "")

        page_data = {
            "page_number": page_num,
            "text": text_content,
            "images": [],  # Placeholder for image extraction
            "tables": table_urls
        }
        all_pages_data.append(page_data)

    # Prepare data to be inserted into MongoDB
    pdf_data = {
        "pdf_name": pdf_name,
        "pages": all_pages_data
    }

    mongo_collection.insert_one(pdf_data)
    print(f"Inserted PDF {pdf_name} into MongoDB.")

def process_pdfs_in_folder(pdf_folder, mongo_collection, storage_client):
    for filename in os.listdir(pdf_folder):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_folder, filename)
            print(f"Processing {filename}...")
            extract_data_from_pdf(pdf_path, mongo_collection, storage_client)

def run_data_extraction_task_closed():
    # MongoDB connection
    client = connect_mongo()
    if client:
        db = client["pdf_database"]
        collection = db["pdf_collection_pdfco_fi"]

        # Local folder to store downloaded PDFs
        local_pdf_folder = "/opt/airflow/dags/data/extracted_pdfs"
        
        # Initialize GCP storage client
        storage_client = storage.Client()

        # Process the PDFs in the specified local folder
        process_pdfs_in_folder(local_pdf_folder, collection, storage_client)

if __name__ == "__main__":
    run_data_extraction_task_closed()
