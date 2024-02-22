from cmd2 import CommandSet, Cmd2ArgumentParser


class BaseCommandSet(CommandSet):

    @staticmethod
    def _get_arg_parser():
        base_arg_parser = Cmd2ArgumentParser()
        base_arg_parser.add_argument(
            "--json",
            help="Output as JSON",
            action="store_true"
        )
        base_arg_parser.add_argument(
            "--csv",
            help="Output as CSV",
            action="store_true"
        )
        return base_arg_parser
