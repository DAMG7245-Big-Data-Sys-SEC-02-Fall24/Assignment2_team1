import os
import shutil

def extract_pdfs(source_dir, destination_dir):
    # Create destination directory if it doesn't exist
    os.makedirs(destination_dir, exist_ok=True)

    # Walk through the source directory and its subdirectories
    for root, _, files in os.walk(source_dir):
        for filename in files:
            if filename.lower().endswith('.pdf'):
                # Construct full file path
                file_path = os.path.join(root, filename)
                # Construct the destination file path
                destination_file_path = os.path.join(destination_dir, filename)
                
                # Check if the file already exists in the destination directory
                if not os.path.exists(destination_file_path):
                    # Copy PDF file to the destination directory
                    shutil.copy(file_path, destination_dir)
                    print(f'Copied: {file_path} to {destination_dir}')
                else:
                    print(f'Skipped (already exists): {filename}')


if __name__ == "__main__":
    source_directory = '/Users/akashvarun/Northeastern/gaia-dataset/'  # Change this to your source directory
    destination_directory = '/Users/akashvarun/Northeastern/gaia-dataset/extracted'  # Change this to your destination directory

    extract_pdfs(source_directory, destination_directory)
