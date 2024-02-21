import json
import requests

from cmd2 import (
    Statement,
    with_argparser,
    with_default_category,
)

from common.BaseCommand import BaseCommand
from common.BaseCommandSet import BaseCommandSet
from common.parse_ioc import IOCUtils
from settings import CRLF, API_URL, API_KEY


@with_default_category("Enrichment")
class EnrichCommandSet(BaseCommandSet):

    enrich_parser = BaseCommandSet._get_arg_parser()
    enrich_parser.add_argument(
        "ioc",
        choices_provider=(lambda self: self._cmd._ioc_cache),
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
        """
        Enriches a domain, IP or URL
        :param params:
        :return:
        """
        if not IOCUtils(params.ioc).validate():
            self._cmd.perror("Not a valid IoC")
            return
        with self.Enrichment(params, self) as enrichment:
            enrichment.enrich()

    class Enrichment(BaseCommand):
        _URL = API_URL + "explore/enrich/{type}/{ioc}/?explain={}&scan_data={}"

        def __enter__(self):
            self._URL = self._URL.format(
                self._params.explain,
                self._params.scan_data,
                type=IOCUtils(self._params.ioc).type,
                ioc=self._params.ioc
            )
            return self

        def enrich(self):
            response = requests.get(
                self._URL,
                headers={"x-api-key": API_KEY}
            )
            self._response = json.loads(response.content).get("response")

        def __exit__(self, exc_type, exc_val, exc_tb):
            super().__exit__(exc_type, exc_val, exc_tb)
            self._commandSet._cmd.poutput(self._output)
            self._commandSet._cmd._add_ioc_to_cache(self._params.ioc)
