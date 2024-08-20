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

    enrich_parser = BaseCommandSet._get_enrich_arg_parser()

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

    bulk_enrich_parser = BaseCommandSet._get_bulk_enrich_arg_parser()

    @with_argparser(bulk_enrich_parser)
    def do_bulk_enrich(self, params: Statement):
        """
        Enriches domains or IPs (ipv4 or ipv6) in a bulk
        You can also use a file as input, i.e.:
            cat to_enrich.txt | xargs sp bulk_enrich
        """
        with self.BulkEnrichment(params, self) as bulk_enrichment:
            bulk_enrichment.enrich()

    class BulkEnrichment(BaseCommand):
        _URL = API_URL + "explore/bulk/summary/{type}?format=json"
        payload = None

        def __enter__(self):
            ioc_type = IOCUtils(self._params.iocs[0]).type
            self._URL = self._URL.format(
                type=ioc_type,
            )
            self._feedback = f"{self._URL[self._URL.index('explore/') + 7:]}"
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
            if self.payload:
                self._response = requests.post(
                    self._URL, json=self.payload, headers={"x-api-key": API_KEY}
                )
            self.check_error()
            self._response = json.loads(self._response.content).get("response")

        def __exit__(self, exc_type, exc_val, exc_tb):
            super().__exit__(exc_type, exc_val, exc_tb)
            self._commandSet._cmd._add_ioc_to_cache(self._params.iocs)
