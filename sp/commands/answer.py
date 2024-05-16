import argparse

import cmd2
from cmd2 import Statement, with_default_category, Cmd2ArgumentParser, with_argparser

from sp.commands.base.padns import PADNS
from sp.commands.base.BaseCmd2ArgumentParser import subcommand_parser
from sp.commands.base.BaseCommandSet import BaseCommandSet
from sp.common.parse_ioc import IOCUtils


@with_default_category("PADNS")
class PADNSAnswerCommandSet(BaseCommandSet):

    _answer_parser = Cmd2ArgumentParser()
    _answer_parser.add_subparsers(
        title="answer",
        help="specify an answer lookup, i.e.: ns"
    )


    @with_argparser(_answer_parser)
    def do_answer(self, ns: argparse.Namespace):
        """
        PADNS Reverse Lookup
        """
        handler = ns.cmd2_handler.get()
        if handler is not None:
            handler(ns)
        else:
            self._cmd.do_help('answer')

    @cmd2.as_subcommand_to('answer', 'a', subcommand_parser)
    def answer_a(self, params: Statement):
        """
        Reverse A lookup
        """
        if not IOCUtils(params.ioc).validate():
            self._cmd.perror("Not a valid IoC")
            return
        with PADNS(params, self, type="answer", qtype="a") as padns:
            padns.lookup()


    @cmd2.as_subcommand_to('answer', 'aaaa', subcommand_parser)
    def answer_aaaa(self, params: Statement):
        """
        Reverse AAAA lookup
        """
        if not IOCUtils(params.ioc).validate():
            self._cmd.perror("Not a valid IoC")
            return
        with PADNS(params, self, type="answer", qtype="aaaa") as padns:
            padns.lookup()


    @cmd2.as_subcommand_to('answer', 'cname', subcommand_parser)
    def answer_cname(self, params: Statement):
        """
        Reverse CNAME lookup
        """
        if not IOCUtils(params.ioc).validate():
            self._cmd.perror("Not a valid IoC")
            return
        with PADNS(params, self, type="answer", qtype="cname") as padns:
            padns.lookup()


    @cmd2.as_subcommand_to('answer', 'mx', subcommand_parser)
    def answer_mx(self, params: Statement):
        """
        Reverse MX lookup
        """
        if not IOCUtils(params.ioc).validate():
            self._cmd.perror("Not a valid IoC")
            return
        with PADNS(params, self, type="answer", qtype="mx") as padns:
            padns.lookup()


    @cmd2.as_subcommand_to('answer', 'ns', subcommand_parser)
    def answer_ns(self, params: Statement):
        """
        Reverse NS lookup
        """
        if not IOCUtils(params.ioc).validate():
            self._cmd.perror("Not a valid IoC")
            return
        with PADNS(params, self, type="answer", qtype="ns") as padns:
            padns.lookup()


    @cmd2.as_subcommand_to('answer', 'ptr4', subcommand_parser)
    def answer_ptr4(self, params: Statement):
        """
        Reverse PTR4 lookup
        """
        if not IOCUtils(params.ioc).validate():
            self._cmd.perror("Not a valid IoC")
            return
        with PADNS(params, self, type="answer", qtype="ptr4") as padns:
            padns.lookup()


    @cmd2.as_subcommand_to('answer', 'ptr6', subcommand_parser)
    def answer_ptr6(self, params: Statement):
        """
        Reverse PTR6 lookup
        """
        if not IOCUtils(params.ioc).validate():
            self._cmd.perror("Not a valid IoC")
            return
        with PADNS(params, self, type="answer", qtype="ptr6") as padns:
            padns.lookup()


    @cmd2.as_subcommand_to('answer', 'soa', subcommand_parser)
    def answer_soa(self, params: Statement):
        """
        Reverse SOA lookup
        """
        if not IOCUtils(params.ioc).validate():
            self._cmd.perror("Not a valid IoC")
            return
        with PADNS(params, self, type="answer", qtype="soa") as padns:
            padns.lookup()


    @cmd2.as_subcommand_to('answer', 'txt', subcommand_parser)
    def answer_txt(self, params: Statement):
        """
        Reverse TXT lookup
        """
        if not IOCUtils(params.ioc).validate():
            self._cmd.perror("Not a valid IoC")
            return
        with PADNS(params, self, type="answer", qtype="txt") as padns:
            padns.lookup()


    @cmd2.as_subcommand_to('answer', 'mxhash', subcommand_parser)
    def answer_mxhash(self, params: Statement):
        """
        Reverse MX Hash lookup
        """
        if not IOCUtils(params.ioc).validate():
            self._cmd.perror("Not a valid IoC")
            return
        with PADNS(params, self, type="answer", qtype="mxhash") as padns:
            padns.lookup()


    @cmd2.as_subcommand_to('answer', 'nshash', subcommand_parser)
    def answer_nshash(self, params: Statement):
        """
        Reverse NS Hash lookup
        """
        if not IOCUtils(params.ioc).validate():
            self._cmd.perror("Not a valid IoC")
            return
        with PADNS(params, self, type="answer", qtype="nshash") as padns:
            padns.lookup()


    @cmd2.as_subcommand_to('answer', 'soahash', subcommand_parser)
    def answer_soahash(self, params: Statement):
        """
        Reverse SOA Hash lookup
        """
        if not IOCUtils(params.ioc).validate():
            self._cmd.perror("Not a valid IoC")
            return
        with PADNS(params, self, type="answer", qtype="soahash") as padns:
            padns.lookup()


    @cmd2.as_subcommand_to('answer', 'txthash', subcommand_parser)
    def answer_txthash(self, params: Statement):
        """
        Reverse TXT Hash lookup
        """
        if not IOCUtils(params.ioc).validate():
            self._cmd.perror("Not a valid IoC")
            return
        with PADNS(params, self, type="answer", qtype="txthash") as padns:
            padns.lookup()
