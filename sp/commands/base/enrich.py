from sp.commands.base.BaseCommand import BaseCommand
from sp.common.exceptions import CommandError, ResponseParseError
from sp.common.parse_ioc import IOCUtils
from sp.common.utils import encode_path_segment
from sp.settings import API_URL


class Enrich(BaseCommand):
    """
    Enrich command
    """

    _URL = API_URL + "v1/enrich/{type}/{ioc}/?format=json"
    """The enrich endpoint URL"""

    def __enter__(self):
        """
        Overrides BaseCommand.__enter__: the logic before executing the command

        :return: Enrich
        """
        self.ioc_type = IOCUtils(self._params.ioc).type
        self._URL = self._URL.format(
            type=self.ioc_type,
            ioc=encode_path_segment(self._params.ioc),
        )
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
        response = self.call_api()
        try:
            self._result = response.get("ip2asn")[0] if self.ioc_type in ["ipv4", "ipv6"] else response
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


class BulkEnrich(BaseCommand):
    """
    Bulk Enrich command
    """

    _URL = API_URL + "v1/enrich/{type}/bulk/"
    """The bulk enrich endpoint URL"""
    payload = None
    """The post payload for the endpoint"""

    def __enter__(self):
        """
        Overrides BaseCommand.__enter__: the logic before executing the command

        :return: BulkEnrich
        """
        self.ioc_type = IOCUtils(self._params.iocs[0]).type
        self._URL = self._URL.format(
            type=self.ioc_type,
        )
        payload_key = "domains"
        if self.ioc_type == "ipv4":
            payload_key = "ipv4s"
        elif self.ioc_type == "ipv6":
            payload_key = "ipv6s"
        if self._params.iocs:
            self.payload = {
                payload_key: list(set(self._params.iocs))
            }
        super().__enter__()
        return self

    def enrich(self):
        """
        The command main logic

        :return: None
        """
        if not self.payload:
            raise CommandError("You need to pass the IoCs")
        response = self.call_api("POST", self.payload).get("response")
        self._result = response.get("ip2asn") if self.ioc_type in ["ipv4", "ipv6"] else response

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
