import os
import requests
import time
import csv
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key and parser ID from environment variables
DOCPARSER_API_KEY = os.getenv('DOCPARSER_API_KEY')
DOCPARSER_PARSER_ID = os.getenv('DOCPARSER_PARSER_ID')
PDF_PATH = os.getenv('PDF_PATH')

def extract_tables_from_pdf(pdf_path):
    # DocParser API endpoint for document upload
    upload_url = f'https://api.docparser.com/v1/document/upload/{DOCPARSER_PARSER_ID}'
    
    # Prepare the file for upload
    with open(pdf_path, 'rb') as file:
        files = {'file': file}
        
        # Make the API request to upload the document
        upload_response = requests.post(
            upload_url,
            files=files,
            headers={'Authorization': f'Basic {DOCPARSER_API_KEY}'}
        )
    
    # Check if the upload was successful
    if upload_response.status_code == 200:
        upload_result = upload_response.json()
        document_id = upload_result.get('id')
        print(f"Upload successful. Document ID: {document_id}")
        
        # Wait for a few seconds to allow DocParser to process the document
        print("Waiting for DocParser to process the document...")
        time.sleep(10)
        
        # Now fetch the parsed results
        fetch_url = f'https://api.docparser.com/v1/results/{DOCPARSER_PARSER_ID}'
        fetch_params = {'document_id': document_id}
        fetch_response = requests.get(
            fetch_url,
            params=fetch_params,
            headers={'Authorization': f'Basic {DOCPARSER_API_KEY}'}
        )
        
        if fetch_response.status_code == 200:
            results = fetch_response.text
            if results:
                print("Successfully retrieved results")
                return results
            else:
                print("No results found. The parser might not have extracted any data.")
                return None
        else:
            print(f"Error fetching results: {fetch_response.status_code}")
            print(f"Response content: {fetch_response.text}")
            return None
    else:
        print(f"Error uploading document: {upload_response.status_code}")
        print(f"Response content: {upload_response.text}")
        return None

def save_to_csv(data, csv_filename):
    parsed_data = json.loads(data)
    
    # Extract the first table (assuming you have a single table or the main table is the first)
    if len(parsed_data) > 0:
        # Assuming the structure you are looking for is within the first table in the JSON
        first_table = parsed_data[0]
        
        # Extract the first key that holds the table rows
        table_data = next((value for key, value in first_table.items() if isinstance(value, list)), [])
        
        if table_data:
            # Dynamically get headers based on the keys of the first row in the table
            headers = table_data[0].keys()
            
            # Open the CSV file and write the data
            with open(csv_filename, mode='w', newline='', encoding='utf-8') as csv_file:
                writer = csv.writer(csv_file)
                
                # Write the header
                writer.writerow(headers)
                
                # Write each row dynamically
                for row in table_data:
                    writer.writerow([row.get(header, '') for header in headers])
            
            print(f"Data successfully saved to {csv_filename}")
        else:
            print("No table data found to write to CSV.")
    else:
        print("Parsed data is empty.")

def main():
    pdf_path = PDF_PATH

    print(f"Attempting to extract tables from: {pdf_path}")

    # Extract tables from PDF
    extracted_data = extract_tables_from_pdf(pdf_path)

    if extracted_data:
        csv_filename = 'extracted_data_1.csv'
        save_to_csv(extracted_data, csv_filename)
    else:
        print("Failed to extract data from the PDF.")

if __name__ == "__main__":
    main()
