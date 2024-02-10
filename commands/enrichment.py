import json
import requests
from typing import List

from cmd2 import (
    Cmd2ArgumentParser,
    CommandSet,
    Statement,
    with_argparser,
    with_default_category,
)

from common.parse_ioc import IOCUtils
from settings import CRLF, API_URL, API_KEY


@with_default_category("Enrichment")
class EnrichmentCommandSet(CommandSet):

    def _url_choices_provider(self) -> List[str]:
        return self._cmd._url_cache

    def _add_url_to_cache(self, url: str) -> None:
        if url not in self._cmd._url_cache:
            self._cmd._url_cache.append(url)

    enrich_parser = Cmd2ArgumentParser()
    enrich_parser.add_argument(
        "ioc",
        choices_provider=_url_choices_provider,
        help="IoC to enrich"
    )
    enrich_parser.add_argument(
        "-explain", type=int, choices=[0, 1], default=0
    )
    enrich_parser.add_argument(
        "-scan_data", type=int, choices=[0, 1], default=0
    )

    @with_argparser(enrich_parser)
    def do_enrich(self, params: Statement):
        if not IOCUtils(params.ioc).validate():
            self._cmd.perror("Not a valid IoC")
            return
        with self.Enrichment(params, self) as enrichment:
            enrichment.enrich()

    class Enrichment:
        enrichmentCommandSet = None
        _BASE_URL = API_URL + "explore/enrich/"
        _URL = _BASE_URL + "{type}/{ioc}/?explain={}&scan_data={}"
        _params = None
        _response = ""
        output = ""

        def __init__(self, params, enrichmentCommandSet):
            self.enrichmentCommandSet = enrichmentCommandSet
            self._URL = self._URL.format(
                params.explain,
                params.scan_data,
                type=IOCUtils(params.ioc).type,
                ioc=params.ioc
            )
            self._params = params
            super(self.__class__, self).__init__()

        def __enter__(self):
            self._response = requests.get(
                self._URL,
                headers={"x-api-key": API_KEY}
            )
            return self

        def enrich(self):
            reply = json.loads(self._response.content).get("response")
            self.output = json.dumps(reply, indent=2) + CRLF

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.enrichmentCommandSet._cmd.poutput(self.output)
            self.enrichmentCommandSet._add_url_to_cache(self._params.ioc)  # Add new url to history cache
