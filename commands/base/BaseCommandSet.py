from cmd2 import CommandSet, Cmd2ArgumentParser


class BaseCommandSet(CommandSet):

    @staticmethod
    def _get_arg_parser():
        base_arg_parser = Cmd2ArgumentParser()
        base_arg_parser.add_argument(
            "ioc",
            choices_provider=(lambda self: self._cmd._ioc_cache),
            help="IoC to enrich"
        )
        base_arg_parser.add_argument(
            "params",
            nargs="*",
            help="parameters to be sent, i.e.: skip=100 limit=10",
            type=str
        )
        base_arg_parser.add_argument(
            "-j",
            "--json",
            help="Output as JSON",
            action="store_true"
        )
        base_arg_parser.add_argument(
            "-c",
            "--csv",
            help="Output as CSV",
            action="store_true"
        )
        base_arg_parser.add_argument(
            "-t",
            "--tsv",
            help="Output as TSV (tab-separated values)",
            action="store_true"
        )
        return base_arg_parser
