import json
import requests

from cmd2 import (
    Statement,
    with_argparser,
    with_default_category,
)

from sp.commands.base.BaseCommand import BaseCommand
from sp.commands.base.BaseCommandSet import BaseCommandSet
from sp.common.parse_ioc import IOCUtils
from sp.settings import API_URL, API_KEY


@with_default_category("Enrichment")
class EnrichCommandSet(BaseCommandSet):

    enrich_parser = BaseCommandSet._get_arg_parser()
    enrich_parser.add_argument("-e", "--explain", action="store_true")
    enrich_parser.add_argument("-s", "--scan_data", action="store_true")

    # @targeted_command
    # @validate_ioc
    @with_argparser(enrich_parser)
    def do_enrich(self, params: Statement):
        """
        Enriches a domain, IP or URL
        """
        with self.Enrichment(params, self) as enrichment:
            enrichment.enrich()

    class Enrichment(BaseCommand):
        _URL = API_URL + "explore/enrich/{type}/{ioc}/?format=json"

        def __enter__(self):
            self._URL = self._URL.format(
                type=IOCUtils(self._params.ioc).type, ioc=self._params.ioc
            )
            self._feedback = f"{self._URL[self._URL.index('explore/') + 7:]}"
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
            self._response = requests.get(self._URL, headers={"x-api-key": API_KEY})
            self.check_error()
            self._response = json.loads(self._response.content).get("response")

        def __exit__(self, exc_type, exc_val, exc_tb):
            super().__exit__(exc_type, exc_val, exc_tb)
            self._commandSet._cmd._add_ioc_to_cache(self._params.ioc)
