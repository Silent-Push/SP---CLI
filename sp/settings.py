import os
from dotenv import load_dotenv

load_dotenv()

CRLF = "\r\n"
API_URL = os.environ.get(
    "SILENT_PUSH_API_URL", "https://app.silentpush.com/api/v1/merge-api/"
)
API_KEY = os.environ.get("SILENT_PUSH_API_KEY")

if API_URL is None:
    raise EnvironmentError(
        "Please set the Silent Push API URL in your environment.\n"
        '\texport SILENT_PUSH_API_URL="'
        'https://app.silentpush.com/api/v1/merge-api/"'
    )

if API_KEY is None:
    raise EnvironmentError(
        "Please set your Silent Push API key in your environment.\n"
        '\texport SILENT_PUSH_API_KEY="YOUR-API-KEY"'
    )
