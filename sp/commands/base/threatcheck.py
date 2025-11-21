import json

import requests

from sp.commands.base.BaseCommand import BaseCommand
from sp.settings import API_KEY, API_URL


class ThreatCheck(BaseCommand):
    """
    ThreatCheck command
    """

    _URL = API_URL + (
        "v2/threat-check?data_source={datasource}&query_type={query_type}"
        "&query={query}&with_cnames={with_cnames}&format=json"
    )
    """The threat check endpoint URL"""

    def __enter__(self):
        """
        The logic before executing the command

        :return: ThreatCheck
        """
        self._URL = self._URL.format(
            datasource=self._params.datasource,
            query_type=self._params.qtype,
            query=self._params.ioc,
            with_cnames=self._params.with_cnames,
        )
        # self._feedback = f"{self._URL[self._URL.index('threat-check') + 12:]}"
        super().__enter__()
        return self

    def check(self):
        """
        The command main logic

        :return: None
        """
        self._response = requests.get(self._URL, headers={"x-api-key": API_KEY})
        self.check_error()
        try:
            if self._params.verbose:
                self._response = json.loads(self._response.content)
                return
            self._response = json.loads(self._response.content).get("listed_details")[0]
        except (json.JSONDecodeError, IndexError) as e:
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


class BulkThreatCheck(BaseCommand):
    """
    Bulk Threat Check command
    """

    _URL = API_URL + "v2/threat-check/bulk?with_cnames={with_cnames}&format=json"
    """The bulk threat check endpoint URL"""
    payload = None
    """The post payload for the threat check endpoint"""

    def __enter__(self):
        """
        The logic before executing the command

        :return: BulkThreatCheck
        """
        self._URL = self._URL.format(with_cnames=self._params.with_cnames)
        self._feedback = f"{self._URL[self._URL.index('threat-check/bulk') + 17:]}"
        if self._params.iocs:
            self.payload = {
                "data_source": self._params.datasource,
                "query_type": self._params.qtype,
                "queries": list(set(self._params.iocs))
            }
        super().__enter__()
        return self

    def check(self):
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
            self._response = json.loads(self._response.content)
            if not self._params.verbose:
                self._response = [
                    {i.get("value"): i.get("listed_details")[0]}
                    for i in self._response
                ]
        except (json.JSONDecodeError, IndexError, AttributeError) as e:
            self._commandSet._cmd.perror(f"Can't parse command response: {e}")

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
