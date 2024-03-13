import json
import requests

from cmd2 import (
    Statement,
    with_argparser,
    with_default_category,
)

from commands.base.BaseCommand import BaseCommand
from commands.base.BaseCommandSet import BaseCommandSet
from common.decorators import targeted_command, validate_ioc
from common.parse_ioc import IOCUtils
from settings import CRLF, API_URL, API_KEY


@with_default_category("Enrichment")
class EnrichCommandSet(BaseCommandSet):

    enrich_parser = BaseCommandSet._get_arg_parser()
    enrich_parser.add_argument(
        "-e", "--explain", action="store_true"
    )
    enrich_parser.add_argument(
        "-s", "--scan_data", action="store_true"
    )

    @targeted_command
    @validate_ioc
    @with_argparser(enrich_parser)
    def do_enrich(self, params: Statement):
        """
        Enriches a domain, IP or URL
        """
        with self.Enrichment(params, self) as enrichment:
            enrichment.enrich()

    class Enrichment(BaseCommand):
        _URL = API_URL + "explore/enrich/{type}/{ioc}/"

        def __enter__(self):
            self._URL = self._URL.format(
                type=IOCUtils(self._params.ioc).type,
                ioc=self._params.ioc
            )
            self._feedback = f"{self._URL[self._URL.index('explore/') + 7:]}"
            if self._params.explain:
                self._params.params.append("explain=1")
            if self._params.scan_data:
                self._params.params.append("scan_data=1")
            super().__enter__()
            return self

        def enrich(self):
            response = requests.get(
                self._URL,
                headers={"x-api-key": API_KEY}
            )
            self._response = json.loads(response.content).get("response")

        def __exit__(self, exc_type, exc_val, exc_tb):
            super().__exit__(exc_type, exc_val, exc_tb)
            self._commandSet._cmd._add_ioc_to_cache(self._params.ioc)
