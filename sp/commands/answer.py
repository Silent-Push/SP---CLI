import argparse

import cmd2
from cmd2 import (Cmd2ArgumentParser, Statement, with_argparser, )

from sp.commands.base.BaseCommandSet import BaseCommandSet
from sp.commands.base.padns import PADNSLookup
from sp.common.parse_ioc import IOCUtils


class PADNSAnswerCommandSet(BaseCommandSet):
    """
    PADNS Answer (Reverse Lookup) Command Set, structured as:
        - **padns**: main command
            - **answer**: sub command of padns command
                - **a**: sub command of answer sub command
                - **aaaa**: sub command of answer sub command
                - ... (more)
    """

    _answer_parser = Cmd2ArgumentParser()
    """The argument parser for the PADNS Answer command, contains a 'sub parser'"""
    _answer_parser.add_subparsers(
        title="answer", help="specify an answer lookup, i.e.: ns"
    )
    subcommand_parser = BaseCommandSet._get_padns_arg_parser()
    """The argument parser for the PADNS Answer sub commands (a, aaaa, ...)"""

    @with_argparser(_answer_parser)
    @cmd2.as_subcommand_to("padns", "answer", subcommand_parser)
    def do_padns_answer(self, ns: argparse.Namespace):
        """
        PADNS Answer (Reverse Lookup) sub command, also contains it's own sub commands

        :param ns: The argument passed to the answer command
        :return: None
        """
        self._cmd.do_help("padns answer")

    @cmd2.as_subcommand_to("padns answer", "a", subcommand_parser)
    def do_padns_answer_a(self, params: Statement):
        """
        Reverse A lookup sub command of answer sub command

        :param params: The passed command parameters
        :return: None
        """
        if not IOCUtils(params.ioc).valid:
            self._cmd.perror("Not a valid IoC")
            return
        with PADNSLookup(params, self, type="answer", qtype="a") as padns:
            padns.lookup()

    @cmd2.as_subcommand_to("padns answer", "aaaa", subcommand_parser)
    def do_padns_answer_aaaa(self, params: Statement):
        """
        Reverse AAAA lookup sub command of answer sub command

        :param params: The passed command parameters
        :return: None
        """
        if not IOCUtils(params.ioc).valid:
            self._cmd.perror("Not a valid IoC")
            return
        with PADNSLookup(params, self, type="answer", qtype="aaaa") as padns:
            padns.lookup()

    @cmd2.as_subcommand_to("padns answer", "cname", subcommand_parser)
    def do_padns_answer_cname(self, params: Statement):
        """
        Reverse CNAME lookup sub command of answer sub command

        :param params: The passed command parameters
        :return: None
        """
        if not IOCUtils(params.ioc).valid:
            self._cmd.perror("Not a valid IoC")
            return
        with PADNSLookup(params, self, type="answer", qtype="cname") as padns:
            padns.lookup()

    @cmd2.as_subcommand_to("padns answer", "mx", subcommand_parser)
    def do_padns_answer_mx(self, params: Statement):
        """
        Reverse MX lookup sub command of answer sub command

        :param params: The passed command parameters
        :return: None
        """
        if not IOCUtils(params.ioc).valid:
            self._cmd.perror("Not a valid IoC")
            return
        with PADNSLookup(params, self, type="answer", qtype="mx") as padns:
            padns.lookup()

    @cmd2.as_subcommand_to("padns answer", "ns", subcommand_parser)
    def do_padns_answer_ns(self, params: Statement):
        """
        Reverse NS lookup sub command of answer sub command

        :param params: The passed command parameters
        :return: None
        """
        if not IOCUtils(params.ioc).valid:
            self._cmd.perror("Not a valid IoC")
            return
        with PADNSLookup(params, self, type="answer", qtype="ns") as padns:
            padns.lookup()

    @cmd2.as_subcommand_to("padns answer", "ptr4", subcommand_parser)
    def do_padns_answer_ptr4(self, params: Statement):
        """
        Reverse PTR4 lookup sub command of answer sub command

        :param params: The passed command parameters
        :return: None
        """
        if not IOCUtils(params.ioc).valid:
            self._cmd.perror("Not a valid IoC")
            return
        with PADNSLookup(params, self, type="answer", qtype="ptr4") as padns:
            padns.lookup()

    @cmd2.as_subcommand_to("padns answer", "ptr6", subcommand_parser)
    def do_padns_answer_ptr6(self, params: Statement):
        """
        Reverse PTR6 lookup sub command of answer sub command

        :param params: The passed command parameters
        :return: None
        """
        if not IOCUtils(params.ioc).valid:
            self._cmd.perror("Not a valid IoC")
            return
        with PADNSLookup(params, self, type="answer", qtype="ptr6") as padns:
            padns.lookup()

    @cmd2.as_subcommand_to("padns answer", "soa", subcommand_parser)
    def do_padns_answer_soa(self, params: Statement):
        """
        Reverse SOA lookup sub command of answer sub command, accepts wildcards

        :param params: The passed command parameters
        :return: None
        """
        with PADNSLookup(params, self, type="answer", qtype="soa") as padns:
            padns.lookup()

    @cmd2.as_subcommand_to("padns answer", "txt", subcommand_parser)
    def do_padns_answer_txt(self, params: Statement):
        """
        Reverse TXT lookup sub command of answer sub command

        :param params: The passed command parameters
        :return: None
        """
        # if not IOCUtils(params.ioc).valid:
        #     self._cmd.perror("Not a valid IoC")
        #     return
        with PADNSLookup(params, self, type="answer", qtype="txt") as padns:
            padns.lookup()

    @cmd2.as_subcommand_to("padns answer", "mxhash", subcommand_parser)
    def do_padns_answer_mxhash(self, params: Statement):
        """
        Reverse MX Hash lookup sub command of answer sub command

        :param params: The passed command parameters
        :return: None
        """
        if not IOCUtils(params.ioc).valid:
            self._cmd.perror("Not a valid IoC")
            return
        with PADNSLookup(params, self, type="answer", qtype="mxhash") as padns:
            padns.lookup()

    @cmd2.as_subcommand_to("padns answer", "nshash", subcommand_parser)
    def do_padns_answer_nshash(self, params: Statement):
        """
        Reverse NS Hash lookup sub command of answer sub command

        :param params: The passed command parameters
        :return: None
        """
        if not IOCUtils(params.ioc).valid:
            self._cmd.perror("Not a valid IoC")
            return
        with PADNSLookup(params, self, type="answer", qtype="nshash") as padns:
            padns.lookup()

    @cmd2.as_subcommand_to("padns answer", "soahash", subcommand_parser)
    def do_padns_answer_soahash(self, params: Statement):
        """
        Reverse SOA Hash lookup sub command of answer sub command

        :param params: The passed command parameters
        :return: None
        """
        if not IOCUtils(params.ioc).valid:
            self._cmd.perror("Not a valid IoC")
            return
        with PADNSLookup(params, self, type="answer", qtype="soahash") as padns:
            padns.lookup()

    @cmd2.as_subcommand_to("padns answer", "txthash", subcommand_parser)
    def do_padns_answer_txthash(self, params: Statement):
        """
        Reverse TXT Hash lookup sub command of answer sub command

        :param params: The passed command parameters
        :return: None
        """
        # if not IOCUtils(params.ioc).valid:
        #     self._cmd.perror("Not a valid IoC")
        #     return
        with PADNSLookup(params, self, type="answer", qtype="txthash") as padns:
            padns.lookup()
