from cmd2 import CommandSet, Cmd2ArgumentParser


class BaseCommandSet(CommandSet):

    @staticmethod
    def _get_arg_parser():
        base_arg_parser = Cmd2ArgumentParser()
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
            "-p",
            "--params",
            nargs="+",
            help="parameters to be sent, i.e.: skip=100 limit=10",
            type=str
        )
        return base_arg_parser
