from cmd2 import Cmd2ArgumentParser, CommandSet


class BaseCommandSet(CommandSet):
    """
    Contains all common methods used for all CommandSet classes
    """

    @staticmethod
    def __set_common_enrich_options(
        enrich_parser: Cmd2ArgumentParser,
    ) -> Cmd2ArgumentParser:
        """
        Set the common options for enrichment commands: -e, -s

        :param enrich_parser: The parser to be overloaded
        :return: Cmd2ArgumentParser
        """
        enrich_parser.add_argument("-e", "--explain", action="store_true")
        enrich_parser.add_argument("-s", "--scan_data", action="store_true")
        return enrich_parser

    @staticmethod
    def __set_common_threatcheck_options(
            threatcheck_parser: Cmd2ArgumentParser,
    ) -> Cmd2ArgumentParser:
        """
        Set the common options for threatcheck commands: -d, -q

        :param threatcheck_parser: The parser to be overloaded
        :return: Cmd2ArgumentParser
        """
        from sp.settings import THREATCHECK_DATASOURCES, THREATCHECK_TYPES

        threatcheck_parser.add_argument(
            "-d",
            "--datasource",
            nargs="?",
            choices_provider=(lambda datasource: THREATCHECK_DATASOURCES),
            default="iofa",
            help="the datasource to threat check, default to 'IOFA'",
        )
        threatcheck_parser.add_argument(
            "-q",
            "--qtype",
            nargs="?",
            choices_provider=(lambda datasource: THREATCHECK_TYPES),
            default="name",
            help="the query type, default to 'name'",
        )
        threatcheck_parser.add_argument(
            "-n",
            "--with_cnames",
            action="store_true",
            default=False,
            help="includes CNAME records in the threat check'",
        )
        return threatcheck_parser

    @staticmethod
    def __set__common_options(parser: Cmd2ArgumentParser) -> Cmd2ArgumentParser:
        """
        Set the 'parameter' options for the majority of the commands: [params...]

        :param parser: The parser to be overloaded
        :return: Cmd2ArgumentParser
        """
        parser.add_argument(
            "params",
            nargs="*",
            help="parameters to be sent, i.e.: skip=100 limit=10",
            type=str,
        )
        return parser

    @staticmethod
    def _get_arg_parser() -> Cmd2ArgumentParser:
        """
        Set the common options for all commands: -j -c -t, -v

        :return: Cmd2ArgumentParser
        """
        base_arg_parser = Cmd2ArgumentParser()
        base_arg_parser.add_argument(
            "-j", "--json", help="Output as JSON", action="store_true"
        )
        base_arg_parser.add_argument(
            "-c", "--csv", help="Output as CSV", action="store_true"
        )
        base_arg_parser.add_argument(
            "-t",
            "--tsv",
            help="Output as TSV (tab-separated values)",
            action="store_true",
        )
        base_arg_parser.add_argument(
            "-v",
            "--verbose",
            action="store_true",
            default=False,
            help="full detailed command response",
        )
        return base_arg_parser

    @staticmethod
    def _get_ioc_arg_parser() -> Cmd2ArgumentParser:
        """
        Set the 'ioc' option for the majority of the commands: [ioc]

        :return: Cmd2ArgumentParser
        """
        ioc_parser = BaseCommandSet._get_arg_parser()
        ioc_parser.add_argument(
            "ioc",
            nargs="?",
            choices_provider=(lambda self: self._cmd._ioc_cache),
            help="IoC to target command",
        )
        return ioc_parser

    @staticmethod
    def _get_score_arg_parser() -> Cmd2ArgumentParser:
        """
        The parser for score command: -j -c -t [ioc] [params...]

        :return: Cmd2ArgumentParser
        """
        score_parser = BaseCommandSet._get_ioc_arg_parser()
        return BaseCommandSet.__set__common_options(score_parser)

    @staticmethod
    def _get_enrich_arg_parser() -> Cmd2ArgumentParser:
        """
        The parser for enrich command: -j -c -t -e -s [ioc] [params...]

        :return:
        """
        enrich_parser = BaseCommandSet._get_ioc_arg_parser()
        enrich_parser = BaseCommandSet.__set_common_enrich_options(enrich_parser)
        return BaseCommandSet.__set__common_options(enrich_parser)

    @staticmethod
    def _get_bulk_enrich_arg_parser() -> Cmd2ArgumentParser:
        """
        The parser for bulk enrich command: -j -c -t -e -s [iocs...] [params...]

        :return:
        """
        bulk_enrich_parser = BaseCommandSet._get_arg_parser()
        bulk_enrich_parser.add_argument(
            "iocs",
            nargs="*",
            choices_provider=(lambda self: self._cmd._ioc_cache),
            help="the list of IoCs to enrich, separated by space, i.e.: "
            "ig.com ibm.com paypal.com",
        )
        bulk_enrich_parser = BaseCommandSet.__set_common_enrich_options(
            bulk_enrich_parser
        )
        return BaseCommandSet.__set__common_options(bulk_enrich_parser)

    @staticmethod
    def _get_threatcheck_arg_parser() -> Cmd2ArgumentParser:
        """
        The parser for threatcheck command: -j -c -t [ioc]

        :return:
        """
        threatcheck_parser = BaseCommandSet._get_ioc_arg_parser()
        return BaseCommandSet.__set_common_threatcheck_options(threatcheck_parser)

    @staticmethod
    def _get_bulk_threatcheck_arg_parser() -> Cmd2ArgumentParser:
        """
        The parser for bulk threatcheck command: -j -c -t [iocs...]

        :return:
        """
        threatcheck_parser = BaseCommandSet._get_arg_parser()
        threatcheck_parser = BaseCommandSet.__set_common_threatcheck_options(threatcheck_parser)
        threatcheck_parser.add_argument(
            "iocs",
            nargs="*",
            choices_provider=(lambda self: self._cmd._ioc_cache),
            help="the list of IoCs to threat check, separated by space, i.e.: "
                 "ig.com ibm.com paypal.com",
        )
        return threatcheck_parser

    @staticmethod
    def _get_padns_arg_parser() -> Cmd2ArgumentParser:
        """
        The parser for PADNS command and sub commands: -j -c -t [ioc] [params...]

        :return:
        """
        padns_parser = BaseCommandSet._get_arg_parser()
        padns_parser.add_argument(
            "ioc",
            nargs="?",
            choices_provider=(lambda self: self._cmd._ioc_cache),
            help="IoC to target command",
        )
        return BaseCommandSet.__set__common_options(padns_parser)

    @staticmethod
    def _get_spql_arg_parser() -> Cmd2ArgumentParser:
        """
        The parser for SPQL commands: -j -c -t [-f [fields...]] [-s [sorts...]] [-d [datasource]] [query] [params...]

        :return: Cmd2ArgumentParser
        """
        from sp.settings import SPQL_DATASOURCES

        spql_parser = BaseCommandSet._get_arg_parser()
        spql_parser.add_argument(
            "query",
            nargs="?",
            type=str,
            # choices_provider=(lambda field: WEBSCAN_FIELDS),
            help='the query to run, i.e.: ""domain"="ig.com""',
        )
        spql_parser = BaseCommandSet.__set__common_options(spql_parser)
        spql_parser.add_argument(
            "-d",
            "--datasource",
            nargs="?",
            choices_provider=(lambda datasource: SPQL_DATASOURCES),
            help="the datasource to query",
        )
        spql_parser.add_argument(
            "-l",
            "--limit",
            type=int,
            help="The number of records to return",
        )
        spql_parser.add_argument("-m", "--with-metadata", action="store_true")
        return spql_parser

    @staticmethod
    def _get_websearch_arg_parser() -> Cmd2ArgumentParser:
        """
        The parser for SPQL Websearch commands: -j -c -t [-f [fields...]] [-s [sorts...]] [-d [datasource]] [query] [params...]

        :return: Cmd2ArgumentParser
        """
        from sp.settings import WEBSCAN_FIELDS

        websearch_parser = BaseCommandSet._get_spql_arg_parser()
        websearch_parser.add_argument(
            "-f",
            "--fields",
            nargs="*",
            choices_provider=(lambda field: WEBSCAN_FIELDS),
            help="the fields to be output",
        )
        websearch_parser.add_argument(
            "-s",
            "--sort",
            nargs="*",
            choices_provider=(lambda field: WEBSCAN_FIELDS),
            help="the sort order (multiple for nested sorting),"
            "i.e.: scan_date/desc domain/asc",
        )
        return websearch_parser

    @staticmethod
    def _get_feedsearch_arg_parser() -> Cmd2ArgumentParser:
        """
        The parser for SPQL Feedsearch commands: -j -c -t [-f [fields...]] [-s [sorts...]] [-d [datasource]] [query] [params...]

        :return: Cmd2ArgumentParser
        """
        from sp.settings import FEEDSCAN_FIELDS

        feedsearch_parser = BaseCommandSet._get_spql_arg_parser()
        feedsearch_parser.add_argument(
            "-f",
            "--fields",
            nargs="*",
            choices_provider=(lambda field: FEEDSCAN_FIELDS),
            help="the fields to be output",
        )
        feedsearch_parser.add_argument(
            "-s",
            "--sort",
            nargs="*",
            choices_provider=(lambda field: FEEDSCAN_FIELDS),
            help="the sort order (multiple for nested sorting),"
            "i.e.: scan_date/desc domain/asc",
        )
        return feedsearch_parser
