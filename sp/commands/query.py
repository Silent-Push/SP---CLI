import argparse

import cmd2
from cmd2 import (Cmd2ArgumentParser, Statement, with_argparser, )

from sp.commands.base.BaseCommandSet import BaseCommandSet
from sp.commands.base.padns import PADNSLookup
from sp.common.parse_ioc import IOCUtils


class PADNSQueryCommandSet(BaseCommandSet):
    """
    PADNS Query (Forward Lookup) Command Set, structured as:
        - **padns**: main command
            - **query**: sub command of padns command
                - **a**: sub command of query sub command
                - **aaaa**: sub command of query sub command
                - ... (more)
    """

    _query_parser = Cmd2ArgumentParser()
    """The argument parser for the PADNS Query command, contains a 'sub parser'"""
    _query_parser.add_subparsers(title="query", help="specify a query lookup, i.e.: ns")
    subcommand_parser = BaseCommandSet._get_padns_arg_parser()
    """The argument parser for the PADNS Query sub commands (a, aaaa, ...)"""

    @with_argparser(_query_parser)
    @cmd2.as_subcommand_to("padns", "query", subcommand_parser)
    def do_padns_query(self, ns: argparse.Namespace):
        """
        PADNS Query (Forward Lookup) sub command, also contains it's own sub commands

        :param ns: The argument passed to the query command
        :return: None
        """
        self._cmd.do_help("padns query")

    # @with_category("Query")
    @cmd2.as_subcommand_to("padns query", "a", subcommand_parser)
    def do_padns_query_a(self, params: Statement):
        """
        Forward A lookup sub command of query sub command

        :param params: The passed command parameters
        :return: None
        """
        with PADNSLookup(params, self, qtype="a") as padns:
            padns.lookup()

    @cmd2.as_subcommand_to("padns query", "aaaa", subcommand_parser)
    def do_padns_query_aaaa(self, params: Statement):
        """
        Forward AAAA lookup sub command of query sub command

        :param params: The passed command parameters
        :return: None
        """
        if not IOCUtils(params.ioc).valid:
            self._cmd.perror("Not a valid IoC")
            return
        with PADNSLookup(params, self, qtype="aaaa") as padns:
            padns.lookup()

    @cmd2.as_subcommand_to("padns query", "cname", subcommand_parser)
    def do_padns_query_cname(self, params: Statement):
        """
        Forward CNAME lookup sub command of query sub command

        :param params: The passed command parameters
        :return: None
        """
        if not IOCUtils(params.ioc).valid:
            self._cmd.perror("Not a valid IoC")
            return
        with PADNSLookup(params, self, qtype="cname") as padns:
            padns.lookup()

    @cmd2.as_subcommand_to("padns query", "mx", subcommand_parser)
    def do_padns_query_mx(self, params: Statement):
        """
        Forward MX lookup sub command of query sub command

        :param params: The passed command parameters
        :return: None
        """
        if not IOCUtils(params.ioc).valid:
            self._cmd.perror("Not a valid IoC")
            return
        with PADNSLookup(params, self, qtype="mx") as padns:
            padns.lookup()

    @cmd2.as_subcommand_to("padns query", "ns", subcommand_parser)
    def do_padns_query_ns(self, params: Statement):
        """
        Forward NS lookup sub command of query sub command

        :param params: The passed command parameters
        :return: None
        """
        if not IOCUtils(params.ioc).valid:
            self._cmd.perror("Not a valid IoC")
            return
        with PADNSLookup(params, self, qtype="ns") as padns:
            padns.lookup()

    @cmd2.as_subcommand_to("padns query", "ptr4", subcommand_parser)
    def do_padns_query_ptr4(self, params: Statement):
        """
        Forward PTR4 lookup sub command of query sub command

        :param params: The passed command parameters
        :return: None
        """
        if not IOCUtils(params.ioc).valid:
            self._cmd.perror("Not a valid IoC")
            return
        with PADNSLookup(params, self, qtype="ptr4") as padns:
            padns.lookup()

    @cmd2.as_subcommand_to("padns query", "ptr6", subcommand_parser)
    def do_padns_query_ptr6(self, params: Statement):
        """
        Forward PTR6 lookup sub command of query sub command

        :param params: The passed command parameters
        :return: None
        """
        if not IOCUtils(params.ioc).valid:
            self._cmd.perror("Not a valid IoC")
            return
        with PADNSLookup(params, self, qtype="ptr6") as padns:
            padns.lookup()

    @cmd2.as_subcommand_to("padns query", "any", subcommand_parser)
    def do_padns_query_any(self, params: Statement):
        """
        Forward Any lookup (combination of A, AAAA, CNAME, PTR, MX and NS)
        sub command of query sub command

        :param params: The passed command parameters
        :return: None
        """
        if not IOCUtils(params.ioc).valid:
            self._cmd.perror("Not a valid IoC")
            return
        with PADNSLookup(params, self, qtype="any") as padns:
            padns.lookup()

    @cmd2.as_subcommand_to("padns query", "anyipv4", subcommand_parser)
    def do_padns_query_anyipv4(self, params: Statement):
        """
        Forward Any IPV4 lookup (combination of PTR and A)
        sub command of query sub command

        :param params: The passed command parameters
        :return: None
        """
        if not IOCUtils(params.ioc).valid:
            self._cmd.perror("Not a valid IoC")
            return
        with PADNSLookup(params, self, qtype="anyipv4") as padns:
            padns.lookup()

    @cmd2.as_subcommand_to("padns query", "anyipv6", subcommand_parser)
    def do_padns_query_anyipv6(self, params: Statement):
        """
        Forward Any IPV6 lookup (combination of PTR and AAAA)
        sub command of query sub command

        :param params: The passed command parameters
        :return: None
        """
        if not IOCUtils(params.ioc).valid:
            self._cmd.perror("Not a valid IoC")
            return
        with PADNSLookup(params, self, qtype="anyipv6") as padns:
            padns.lookup()

    @cmd2.as_subcommand_to("padns query", "soa", subcommand_parser)
    def do_padns_query_soa(self, params: Statement):
        """
        Forward SOA lookup sub command of query sub command

        :param params: The passed command parameters
        :return: None
        """
        if not IOCUtils(params.ioc).valid:
            self._cmd.perror("Not a valid IoC")
            return
        with PADNSLookup(params, self, qtype="soa") as padns:
            padns.lookup()

    @cmd2.as_subcommand_to("padns query", "txt", subcommand_parser)
    def do_padns_query_txt(self, params: Statement):
        """
        Forward TXT lookup sub command of query sub command

        :param params: The passed command parameters
        :return: None
        """
        if not IOCUtils(params.ioc).valid:
            self._cmd.perror("Not a valid IoC")
            return
        with PADNSLookup(params, self, qtype="txt") as padns:
            padns.lookup()
