from cmd2 import CommandSet, Cmd2ArgumentParser


class BaseCommandSet(CommandSet):
    @staticmethod
    def __set_common_enrich_options(enrich_parser):
        enrich_parser.add_argument("-e", "--explain", action="store_true")
        enrich_parser.add_argument("-s", "--scan_data", action="store_true")
        return enrich_parser

    @staticmethod
    def __set__common_options(parser):
        parser.add_argument(
            "params",
            nargs="*",
            help="parameters to be sent, i.e.: skip=100 limit=10",
            type=str,
        )
        return parser

    @staticmethod
    def _get_arg_parser():
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
        return base_arg_parser

    @staticmethod
    def _get_ioc_arg_parser():
        ioc_parser = BaseCommandSet._get_arg_parser()
        ioc_parser.add_argument(
            "ioc",
            nargs="?",
            choices_provider=(lambda self: self._cmd._ioc_cache),
            help="IoC to target command",
        )
        return ioc_parser

    @staticmethod
    def _get_score_arg_parser():
        score_parser = BaseCommandSet._get_ioc_arg_parser()
        return BaseCommandSet.__set__common_options(score_parser)

    @staticmethod
    def _get_enrich_arg_parser():
        enrich_parser = BaseCommandSet._get_ioc_arg_parser()
        enrich_parser = BaseCommandSet.__set_common_enrich_options(enrich_parser)
        return BaseCommandSet.__set__common_options(enrich_parser)

    @staticmethod
    def _get_bulk_enrich_arg_parser():
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
    def _get_padns_arg_parser():
        padns_parser = BaseCommandSet._get_arg_parser()
        padns_parser.add_argument(
            "ioc",
            nargs="?",
            choices_provider=(lambda self: self._cmd._ioc_cache),
            help="IoC to target command",
        )
        return BaseCommandSet.__set__common_options(padns_parser)

    @staticmethod
    def _get_spql_webscan_arg_parser():
        from sp.settings import WEBSCAN_FIELDS, SPQL_DATASOURCES

        spql_webscan_parser = BaseCommandSet._get_arg_parser()
        spql_webscan_parser.add_argument(
            "query",
            nargs="?",
            # choices_provider=(lambda field: WEBSCAN_FIELDS),
            help='the query to run, i.e.: "\"domain\"=\"ig.com\""',
        )
        spql_webscan_parser = BaseCommandSet.__set__common_options(
            spql_webscan_parser
        )
        spql_webscan_parser.add_argument(
            "-f",
            "--fields",
            nargs="*",
            choices_provider=(lambda field: WEBSCAN_FIELDS),
            help="the fields to be output",
        )
        spql_webscan_parser.add_argument(
            "-s",
            "--sort",
            nargs="*",
            choices_provider=(lambda field: WEBSCAN_FIELDS),
            help="the sort order (multiple for nested sorting),"
                 "i.e.: scan_date/desc domain/asc",
        )
        spql_webscan_parser.add_argument(
            "-d",
            "--datasource",
            nargs="?",
            choices_provider=(lambda datasource: SPQL_DATASOURCES),
            help="the datasource to query",
        )
        return spql_webscan_parser
