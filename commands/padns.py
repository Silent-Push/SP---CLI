import argparse
import json
import requests

from cmd2 import (
    Statement,
    with_argparser,
    with_default_category, cmd2, Cmd2ArgumentParser,
)

from common.BaseCommand import BaseCommand
from common.BaseCommandSet import BaseCommandSet
from common.parse_ioc import IOCUtils
from settings import CRLF, API_URL, API_KEY


@with_default_category("PADNS")
class PADNScommandSet(BaseCommandSet):

    _padns_parser = BaseCommandSet._get_arg_parser()
    _padns_parser.add_subparsers(title="query", help="specify a query, i.e.: ns")

    @with_argparser(_padns_parser)
    def do_padns(self, ns: argparse.Namespace):
        """
        PADNS Lookup
        :param ns:
        :return:
        """
        handler = ns.cmd2_handler.get()
        if handler is not None:
            handler(ns)
        else:
            self.do_help('padns')

    _ns_parser = Cmd2ArgumentParser()
    _ns_parser.add_argument(
        "ioc",
        choices_provider=(lambda self: self._cmd._ioc_cache),
        help="IoC to lookup")

    @cmd2.as_subcommand_to('padns', 'ns', _ns_parser)
    def padns_ns(self, _: argparse.Namespace):
        self._cmd.poutput("PADNS ns")