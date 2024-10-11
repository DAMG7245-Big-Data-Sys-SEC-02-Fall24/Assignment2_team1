import pdfplumber
import os
import csv

input_pdf_path = input("Enter the path to your PDF file: ")

with pdfplumber.open(input_pdf_path) as pdf:
    for page_number in range(len(pdf.pages)):
        page = pdf.pages[page_number]
        
        # Extract tables
        tables = page.extract_tables()
        for i, table in enumerate(tables):
            print(f"Table {i+1} on Page {page_number + 1}:")
            csv_filename = f'table_{page_number + 1}_{i + 1}.csv'
            with open(csv_filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                for row in table:
                    writer.writerow(row)
            print(f"Saved table {i+1} on Page {page_number + 1} to {csv_filename}")

print("Extraction complete.")

