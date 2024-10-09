import requests
import os 
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('DOCPARSER_API_KEY')
url = 'https://api.docparser.com/v1/parsers'

response = requests.get(url, headers={'Authorization': f'Basic {api_key}'})
print(response.status_code)
print(response.json())