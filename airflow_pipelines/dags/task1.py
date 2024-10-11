from huggingface_hub import snapshot_download, login
import subprocess
import os
from dotenv import load_dotenv

load_dotenv()

# Replace 'your_token_here' with your actual Hugging Face token
HF_TOKEN = os.getenv('HF_TOKEN')

def login_to_hf():
    try:
        # Pass the token explicitly to avoid any interactive input
        login(token=HF_TOKEN, add_to_git_credential=True)
        print("Successfully logged in to Hugging Face")
    except Exception as e:
        print(f"Failed to log in: {e}")

def clone_repository_with_hf(repo_id, destination_folder):
    try:
        # Ensure the destination folder exists
        os.makedirs(destination_folder, exist_ok=True)
        
        # Use snapshot_download to download the entire dataset repository
        snapshot_download(repo_id=repo_id, local_dir=destination_folder, repo_type="dataset")
        print(f"Successfully downloaded {repo_id} into {destination_folder}")
    except Exception as e:
        print(f"Failed to download repository: {e}")

# Repository ID and local folder path
repo_id = "gaia-benchmark/GAIA"  # Use only the repo id, not the full URL
destination_folder = "/opt/airflow/dags/data/GAIA-dataset"  # Ensure this path is writable


def run_task():
    # First, login to Hugging Face
    login_to_hf()
    # Then, clone the repository
    clone_repository_with_hf(repo_id, destination_folder)