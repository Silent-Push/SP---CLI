import os
from dotenv import load_dotenv

load_dotenv()

CRLF = "\r\n"
API_URL = os.environ.get("API_URL")
API_KEY = os.environ.get("API_KEY")