from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os 
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
mongo_uri = os.getenv("MONGO_URI")
# Function to test MongoDB connection
def test_mongo_connection():
    try:
        # Replace with your MongoDB URI
        client = MongoClient(mongo_uri)  
        
        # Test the connection by attempting to get server info
        client.admin.command('ping')
        print("MongoDB connection successful.")
        
    except ConnectionFailure as e:
        print(f"Could not connect to MongoDB: {e}")

# Test the connection
test_mongo_connection()
