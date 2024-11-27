import argparse

import cmd2
from cmd2 import Statement, with_default_category, with_argparser

from sp.commands.base.spql import SPQL
from sp.commands.base.BaseCommandSet import BaseCommandSet


@with_default_category("SPQL")
class SPQLWebscanCommandSet(BaseCommandSet):
    """
   SPQL Webscan Command Set, structured as:
        - **spql**: main command
            - **webscan**: sub command of spql command
            - ... (more to come)
    """

    spql_parser = cmd2.Cmd2ArgumentParser()
    """The argument parser for the SPQL command, contains a 'sub parser'"""
    spql_parser.add_subparsers(
        title="SPQL command",
        help="Silent Push Query Language, "
             "see: https://help.silentpush.com/docs/spql"
    )

    @with_argparser(spql_parser)
    def do_spql(self, ns: argparse.Namespace):
        """
        SPQL - Silent Push Query Language command

        :param ns: The argument passed to the query command
        :return: None
        """
        handler = ns.cmd2_handler.get()
        if handler is not None:
            try:
                handler(ns)
            except TypeError:
                # self.perror(e)
                self.do_help("spql")
        else:
            # No subcommand was provided, so call help
            self.do_help("spql")

    spql_webscan_parser = BaseCommandSet._get_spql_webscan_arg_parser()
    """The argument parser for the SPQL Webscan sub command"""

    @cmd2.as_subcommand_to("spql", "webscan", spql_webscan_parser)
    def spql_webscan(self, params: Statement):
        """
        SPQL Webscan

        :param params: The passed command parameters
        :return: None
        """
        with SPQL(params, self) as spql:
            spql.scan()
