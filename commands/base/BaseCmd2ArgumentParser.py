from cmd2 import Cmd2ArgumentParser

from commands.base.BaseCommandSet import BaseCommandSet

subcommand_parser = BaseCommandSet._get_arg_parser()
subcommand_parser.add_argument(
    "ioc",
    choices_provider=(lambda self: self._cmd._ioc_cache),
    type=str,
    help="IoC to lookup"
)