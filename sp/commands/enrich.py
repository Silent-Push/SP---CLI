from cmd2 import Statement, with_argparser, with_default_category

from sp.commands.base.BaseCommandSet import BaseCommandSet
from sp.commands.base.enrich import BulkEnrich, Enrich
from sp.common.parse_ioc import IOCUtils


@with_default_category("Enrichment")
class EnrichCommandSet(BaseCommandSet):
    """
    Enrich Command Set
    """

    enrich_parser = BaseCommandSet._get_enrich_arg_parser()
    """The argument parser for the enrich command"""

    @with_argparser(enrich_parser)
    def do_enrich(self, params: Statement):
        """
        Enriches a domain, IP or URL

        :param params: The passed command parameters
        :return: None
        """
        if not IOCUtils(params.ioc).valid:
            self._cmd.perror("Not a valid IoC")
            return
        with Enrich(params, self) as enrichment:
            enrichment.enrich()

    bulk_enrich_parser = BaseCommandSet._get_bulk_enrich_arg_parser()
    """The argument parser for the bulk_enrich command"""

    @with_argparser(bulk_enrich_parser)
    def do_bulk_enrich(self, params: Statement):
        """
        | Enriches domains or IPs (ipv4 or ipv6) in a bulk
        | You can also use a file as input, i.e.:
        |   ``cat to_enrich.txt | xargs sp bulk_enrich``

        :param params: The passed command parameters
        :return: None
        """
        with BulkEnrich(params, self) as bulk_enrichment:
            bulk_enrichment.enrich()
