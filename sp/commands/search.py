import argparse

import cmd2
from cmd2 import Statement, Cmd2ArgumentParser, with_argparser, with_default_category

from sp.commands.base.padns import PADNSSearch
from sp.commands.base.BaseCommandSet import BaseCommandSet
from sp.common.parse_ioc import IOCUtils


@with_default_category("PADNS")
class PADNSSearchCommandSet(BaseCommandSet):
    """
    PADNS Search Command Set, structured as:
        - **padns**: main command
            - **search**: sub command of padns command
                - **ipdiversity**: sub command of search sub command
                - ... (more)
    """

    _search_parser = Cmd2ArgumentParser()
    """The argument parser for the PADNS Search command, contains a 'sub parser'"""
    _search_parser.add_subparsers(title="search", help="specify a search lookup, i.e.: ipdiversity")
    subcommand_parser = BaseCommandSet._get_padns_arg_parser()
    """The argument parser for the PADNS Search sub commands (ipdiversity, selfhosted, ...)"""

    @with_argparser(_search_parser)
    @cmd2.as_subcommand_to("padns", "search", subcommand_parser)
    def do_search(self, ns: argparse.Namespace):
        """
        PADNS Search sub command, also contains it's own sub commands

        :param ns: The argument passed to the search command
        :return: None
        """
        self._cmd.do_help("search")

    @cmd2.as_subcommand_to("search", "ipdiversity", subcommand_parser)
    def search_ipdiversity(self, params: Statement):
        """
        IP Diversity sub command of search command

        :param params: The passed command parameters
        :return: None
        """
        if not IOCUtils(params.ioc).valid:
            self._cmd.perror("Search Not a valid IoC")
            return
        with PADNSSearch(params, self, type="ipdiversity") as padns:
            padns.lookup()
