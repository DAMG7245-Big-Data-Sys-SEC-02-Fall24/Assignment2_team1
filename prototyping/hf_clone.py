from huggingface_hub import snapshot_download
from huggingface_hub import login
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

hf_token = os.getenv('HF_TOKEN')

# Replace 'your_token_here' with your actual Hugging Face token
login(token=hf_token)

def clone_repository_with_hf(repo_name, destination_folder):
    try:
        # Use snapshot_download to download the entire dataset repository
        snapshot_download(repo_id=repo_name, local_dir=destination_folder, repo_type="dataset")
        print(f"Successfully downloaded {repo_name} into {destination_folder}")
    except Exception as e:
        print(f"Failed to download repository: {e}")

# Repository name and local folder path
repo_name = "gaia-benchmark/GAIA"  # Adjusted to just the name
destination_folder = "./GAIA-dataset"

# Clone the repository using the Hugging Face Hub
clone_repository_with_hf(repo_name, destination_folder)
