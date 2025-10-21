import json

import requests

from sp.commands.base.BaseCommand import BaseCommand
from sp.common.parse_ioc import IOCUtils
from sp.settings import API_KEY, API_URL


class Enrich(BaseCommand):
    """
    Enrich command
    """

    _URL = API_URL + "v1/merge-api/explore/enrich/{type}/{ioc}/?format=json"
    """The enrich endpoint URL"""

    def __enter__(self):
        """
        The logic before executing the command

        :return: Enrich
        """
        self._URL = self._URL.format(
            type=IOCUtils(self._params.ioc).type, ioc=self._params.ioc
        )
        # self._feedback = f"{self._URL[self._URL.index('explore/') + 7:]}"
        if self._params.explain:
            self._params.params.append("explain=1")
        else:
            self._params.params.append("explain=0")
        if self._params.scan_data:
            self._params.params.append("scan_data=1")
        else:
            self._params.params.append("scan_data=0")
        super().__enter__()
        return self

    def enrich(self):
        """
        The command main logic

        :return: None
        """
        self._response = requests.get(self._URL, headers={"x-api-key": API_KEY})
        self.check_error()
        try:
            self._response = json.loads(self._response.content).get("response")
        except json.JSONDecodeError as e:
            self._commandSet._cmd.perror(f"Can't parse command response: {e.msg}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        The logic after executing the command

        :param exc_type: Exception type, if need to catch
        :param exc_val: Exception value
        :param exc_tb: Exception trac
        """
        super().__exit__(exc_type, exc_val, exc_tb)
        self._commandSet._cmd._add_ioc_to_cache(self._params.ioc)


class BulkEnrich(BaseCommand):
    """
    Bulk Enrich command
    """

    _URL = API_URL + "v1/merge-api/explore/bulk/summary/{type}?format=json"
    """The bulk enrich endpoint URL"""
    payload = None
    """The post payload for the endpoint"""

    def __enter__(self):
        """
        The logic before executing the command

        :return: BulkEnrich
        """
        ioc_type = IOCUtils(self._params.iocs[0]).type
        self._URL = self._URL.format(
            type=ioc_type,
        )
        # self._feedback = f"{self._URL[self._URL.index('explore/') + 7:]}"
        if self._params.iocs:
            self.payload = {
                "domains"
                if ioc_type == "domain"
                else "ips": list(set(self._params.iocs))
            }
        if self._params.explain:
            self._params.params.append("explain=1")
        else:
            self._params.params.append("explain=0")
        if self._params.scan_data:
            self._params.params.append("scan_data=1")
        else:
            self._params.params.append("scan_data=0")
        super().__enter__()
        return self

    def enrich(self):
        """
        The command main logic

        :return: None
        """
        if self.payload:
            self._response = requests.post(
                self._URL, json=self.payload, headers={"x-api-key": API_KEY}
            )
        self.check_error()
        try:
            self._response = json.loads(self._response.content).get("response")
        except json.JSONDecodeError as e:
            self._commandSet._cmd.perror(f"Can't parse command response: {e.msg}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        The logic after executing the command

        :param exc_type: Exception type, if need to catch
        :param exc_val: Exception value
        :param exc_tb: Exception traceback
        :return: None
        """
        super().__exit__(exc_type, exc_val, exc_tb)
        self._commandSet._cmd._add_ioc_to_cache(self._params.iocs)
