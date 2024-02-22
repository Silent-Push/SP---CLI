from cmd2 import Cmd2ArgumentParser

from commands.base.BaseCommandSet import BaseCommandSet

baseCmd2ArgumentParser = Cmd2ArgumentParser()
baseCmd2ArgumentParser.add_argument(
    "--json",
    help="Output as JSON"
)
baseCmd2ArgumentParser.add_argument(
    "--csv",
    help="Output as CSV"
)

subcommand_parser = BaseCommandSet._get_arg_parser()
subcommand_parser.add_argument(
    "ioc",
    choices_provider=(lambda self: self._cmd._ioc_cache),
    help="IoC to lookup"
)