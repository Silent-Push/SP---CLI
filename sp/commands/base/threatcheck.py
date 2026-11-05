from sp.commands.base.BaseCommand import BaseCommand
from sp.common.exceptions import CommandError, ResponseParseError
from sp.common.utils import encode_query_value
from sp.settings import API_URL


class ThreatCheck(BaseCommand):
    """
    ThreatCheck command
    """

    _URL = API_URL + (
        "v1/threat-check?data_source={datasource}&query_type={query_type}"
        "&query={query}&with_cnames={with_cnames}&format=json"
    )
    """The threat check endpoint URL"""

    def __enter__(self):
        """
        Overrides BaseCommand.__enter__: the logic before executing the command

        :return: ThreatCheck
        """
        self._URL = self._URL.format(
            datasource=encode_query_value(self._params.datasource),
            query_type=encode_query_value(self._params.qtype),
            query=encode_query_value(self._params.ioc),
            with_cnames=self._params.with_cnames,
        )
        super().__enter__()
        return self

    def check(self):
        """
        The command main logic

        :return: None
        """
        self._result = response = self.call_api()
        if self._params.verbose:
            return
        try:
            self._result = response.get("listed_details")[0]
        except (IndexError, TypeError) as e:
            raise ResponseParseError(e)

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Overrides BaseCommand.__exit__: the logic after executing the command

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

    _URL = API_URL + "v1/threat-check/bulk?with_cnames={with_cnames}&format=json"
    """The bulk threat check endpoint URL"""
    payload = None
    """The post payload for the threat check endpoint"""

    def __enter__(self):
        """
        Overrides BaseCommand.__enter__: the logic before executing the command

        :return: BulkThreatCheck
        """
        self._URL = self._URL.format(with_cnames=self._params.with_cnames)
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
        if not self.payload:
            raise CommandError("You need to pass the IoCs")
        self._result = response = self.call_api("POST", self.payload)
        if self._params.verbose:
            return
        try:
            self._result = [
                {i.get("value"): i.get("listed_details")[0]}
                for i in response
            ]
        except (IndexError, AttributeError) as e:
            raise ResponseParseError(e)

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Overrides BaseCommand.__exit__: the logic after executing the command

        :param exc_type: Exception type, if need to catch
        :param exc_val: Exception value
        :param exc_tb: Exception traceback
        :return: None
        """
        super().__exit__(exc_type, exc_val, exc_tb)
        self._commandSet._cmd._add_ioc_to_cache(self._params.iocs)
