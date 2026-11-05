from sp.commands.base.BaseCommand import BaseCommand
from sp.common.exceptions import CommandError
from sp.common.utils import encode_path_segment
from sp.settings import API_URL


class WhoisLive(BaseCommand):
    """
    WhoisLive command: Get real-time whois information for domain
    """

    _URL = API_URL + "v1/explore/domain/whoislive/{domain}/"
    """The whoislive endpoint URL"""

    def __enter__(self):
        """
        Overrides BaseCommand.__enter__: the logic before executing the command

        :return: WhoisLive
        """
        self._URL = self._URL.format(domain=encode_path_segment(self._params.domain))
        super().__enter__()
        return self

    def search(self):
        """
        The command main logic

        :return: None
        """
        self._result = (self.call_api().get("response", {}) or {}).get("whois_live")
        if not self._result:
            raise CommandError(f"No whois information found for {self._params.domain}")

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Overrides BaseCommand.__exit__: the logic after executing the command

        :param exc_type: Exception type, if need to catch
        :param exc_val: Exception value
        :param exc_tb: Exception traceback
        """
        super().__exit__(exc_type, exc_val, exc_tb)
        self._commandSet._cmd._add_ioc_to_cache(self._params.domain)
