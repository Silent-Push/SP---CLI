import argparse

import cmd2
from cmd2 import Statement, Cmd2ArgumentParser, with_argparser, with_default_category

from commands.base.padns import PADNS
from commands.base.BaseCmd2ArgumentParser import subcommand_parser
from commands.base.BaseCommandSet import BaseCommandSet
from common.decorators import targeted_command, validate_ioc
from common.parse_ioc import IOCUtils


@with_default_category("PADNS")
class PADNSQueryCommandSet(BaseCommandSet):

    _query_parser = Cmd2ArgumentParser()
    _query_parser.add_subparsers(
        title="query",
        help="specify a query lookup, i.e.: ns"
    )

    @with_argparser(_query_parser)
    def do_query(self, ns: argparse.Namespace):
        """
        PADNS Forward Lookup
        """
        handler = ns.cmd2_handler.get()
        if handler is not None:
            handler(ns)
        else:
            self._cmd.do_help('query')

    @targeted_command
    @validate_ioc
    @cmd2.as_subcommand_to('query', 'a', subcommand_parser)
    def query_a(self, params: Statement):
        """
        Forward A lookup
        """
        with PADNS(params, self, qtype="a") as padns:
            padns.lookup()


    @cmd2.as_subcommand_to('query', 'aaaa', subcommand_parser)
    def query_aaaa(self, params: Statement):
        """
        Forward AAAA lookup
        """
        if not IOCUtils(params.ioc).validate():
            self._cmd.perror("Not a valid IoC")
            return
        with PADNS(params, self, qtype="aaaa") as padns:
            padns.lookup()


    @cmd2.as_subcommand_to('query', 'cname', subcommand_parser)
    def query_cname(self, params: Statement):
        """
        Forward CNAME lookup
        """
        if not IOCUtils(params.ioc).validate():
            self._cmd.perror("Not a valid IoC")
            return
        with PADNS(params, self, qtype="cname") as padns:
            padns.lookup()


    @cmd2.as_subcommand_to('query', 'mx', subcommand_parser)
    def query_mx(self, params: Statement):
        """
        Forward MX lookup
        """
        if not IOCUtils(params.ioc).validate():
            self._cmd.perror("Not a valid IoC")
            return
        with PADNS(params, self, qtype="mx") as padns:
            padns.lookup()


    @cmd2.as_subcommand_to('query', 'ns', subcommand_parser)
    def query_ns(self, params: Statement):
        """
        Forward NS lookup
        """
        if not IOCUtils(params.ioc).validate():
            self._cmd.perror("Not a valid IoC")
            return
        with PADNS(params, self, qtype="ns") as padns:
            padns.lookup()


    @cmd2.as_subcommand_to('query', 'ptr4', subcommand_parser)
    def query_ptr4(self, params: Statement):
        """
        Forward PTR4 lookup
        """
        if not IOCUtils(params.ioc).validate():
            self._cmd.perror("Not a valid IoC")
            return
        with PADNS(params, self, qtype="ptr4") as padns:
            padns.lookup()


    @cmd2.as_subcommand_to('query', 'ptr6', subcommand_parser)
    def query_ptr6(self, params: Statement):
        """
        Forward PTR6 lookup
        """
        if not IOCUtils(params.ioc).validate():
            self._cmd.perror("Not a valid IoC")
            return
        with PADNS(params, self, qtype="ptr6") as padns:
            padns.lookup()


    @cmd2.as_subcommand_to('query', 'any', subcommand_parser)
    def query_any(self, params: Statement):
        """
        Forward Any lookup (combination of A, AAAA, CNAME, PTR, MX and NS)
        """
        if not IOCUtils(params.ioc).validate():
            self._cmd.perror("Not a valid IoC")
            return
        with PADNS(params, self, qtype="any") as padns:
            padns.lookup()


    @cmd2.as_subcommand_to('query', 'anyipv4', subcommand_parser)
    def query_anyipv4(self, params: Statement):
        """
        Forward Any IPV4 lookup (combination of PTR and A)
        """
        if not IOCUtils(params.ioc).validate():
            self._cmd.perror("Not a valid IoC")
            return
        with PADNS(params, self, qtype="anyipv4") as padns:
            padns.lookup()


    @cmd2.as_subcommand_to('query', 'anyipv6', subcommand_parser)
    def query_anyipv6(self, params: Statement):
        """
        Forward Any IPV6 lookup (combination of PTR and AAAA)
        """
        if not IOCUtils(params.ioc).validate():
            self._cmd.perror("Not a valid IoC")
            return
        with PADNS(params, self, qtype="anyipv6") as padns:
            padns.lookup()


    @cmd2.as_subcommand_to('query', 'soa', subcommand_parser)
    def query_soa(self, params: Statement):
        """
        Forward SOA lookup
        """
        if not IOCUtils(params.ioc).validate():
            self._cmd.perror("Not a valid IoC")
            return
        with PADNS(params, self, qtype="soa") as padns:
            padns.lookup()


    @cmd2.as_subcommand_to('query', 'txt', subcommand_parser)
    def query_txt(self, params: Statement):
        """
        Forward TXT lookup
        """
        if not IOCUtils(params.ioc).validate():
            self._cmd.perror("Not a valid IoC")
            return
        with PADNS(params, self, qtype="txt") as padns:
            padns.lookup()
