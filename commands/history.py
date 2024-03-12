import json
import requests

from cmd2 import (
    Statement,
    with_argparser,
    with_default_category, Cmd2ArgumentParser,
)

from commands.base.BaseCommand import BaseCommand
from commands.base.BaseCommandSet import BaseCommandSet
from common.parse_ioc import IOCUtils
from settings import CRLF, API_URL, API_KEY


@with_default_category("History")
class HistoryCommandSet(BaseCommandSet):

    history_parser = Cmd2ArgumentParser()
    history_parser.add_argument(
        "-hs",
        "--history",
        help="shows the last {n} commands",
        type=int
    )


    # @TODO: extend builtin history
    @with_argparser(history_parser)
    def do_last_history(self, params: Statement):
        """
        Shows last {n} commands from history
        """
        last_commands = self._commandSet._cmd._get_iocs_from_history()[
           :self._params.history
        ]
        self._commandSet._cmd.poutput(last_commands)
