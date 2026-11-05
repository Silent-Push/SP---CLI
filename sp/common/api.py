from importlib.metadata import PackageNotFoundError, version

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from sp import settings

try:
    USER_AGENT = f"SP-CLI/{version('SilentPushCLI')}"
except PackageNotFoundError:  # running from the source folder, not installed
    USER_AGENT = "SP-CLI/dev"
"""Sent on every request so the API team can see CLI traffic"""

RETRY_STATUSES = (429, 500, 502, 503, 504)
"""Rate limited or server errors, worth trying again"""


class ApiClient:
    """
    Persistent HTTP session shared by all commands, more useful in interactive mode
    """

    def __init__(self):
        retry = Retry(
            total=3,
            backoff_factor=1,  # waits 1s, 2s, 4s between tries
            status_forcelist=RETRY_STATUSES,
            allowed_methods=None,  # also retry POST
            respect_retry_after_header=True,
            raise_on_status=False,  # return the last response so BaseCommand can show the error
        )
        self.session = requests.Session()
        self.session.mount("https://", HTTPAdapter(max_retries=retry))
        self.session.mount("http://", HTTPAdapter(max_retries=retry))
        self.session.headers["User-Agent"] = USER_AGENT

    def request(self, method: str, url: str, payload: dict = None) -> requests.Response:
        """
        Calls the Silent Push API

        :param method: GET or POST
        :param url: The full endpoint URL
        :param payload: The JSON body for POST requests
        :return: The API response
        :raises requests.RequestException: On timeout or connection errors
        """
        return self.session.request(
            method,
            url,
            json=payload,
            # read at call time, so tests and a late `export` still work
            headers={"x-api-key": settings.API_KEY},
            timeout=settings.API_TIMEOUT,
        )


api = ApiClient()
"""The client used by all commands"""
