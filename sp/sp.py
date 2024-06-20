#!/usr/bin/env python3
# coding=utf-8
import argparse
import cmd2
from typing import List

__app_name__ = "SP-CLI"

from cmd2 import with_category, CommandSetRegistrationError

from sp.common.utils import AppFileManager
from sp.commands import *


class App(cmd2.Cmd):
    intro = "Silent Push - CLI"
    prompt = "SP# "
    PREPEND_COMMANDS = ["padns", "query", "answer"]

    def __init__(self, **kwargs):
        self.app_man = kwargs.get("application_manager")
        hist_file = self.app_man.hist_file
        super().__init__(
            persistent_history_file=hist_file,
            persistent_history_length=500,
            auto_load_commands=False,
            allow_cli_args=False  # we use our own argparse,
        )
        # Create a cache object to save url information to
        self._ioc_cache: List = self._get_iocs_from_history()
        self._query = PADNSQueryCommandSet()
        self._answer = PADNSAnswerCommandSet()
        self.register_command_set(EnrichCommandSet())
        # self.register_command_set(HistoryCommandSet())
        self.register_command_set(ScoreCommandSet())
        self.register_postparsing_hook(self.prepend_padns_main_command_hook)

    def prepend_padns_main_command_hook(
            self, data: cmd2.plugin.PostparsingData
    ) -> cmd2.plugin.PostparsingData:
        """
        Automatiically adds 'padns' to the subcommands so user can type just
        'query a...' rather than 'padns query a...'
        """
        command = data.statement.command
        rest_args = data.statement.args
        post_command = data.statement.post_command
        # self.poutput(f"got command: {command}, {rest_args}, {post_command}")
        if command not in self.PREPEND_COMMANDS:
            return data
        try:
            if command == "padns":
                # self.poutput("prepend padns hook")
                self.register_command_set(self._query)
                self.register_command_set(self._answer)
            elif command == "query" or rest_args.startswith("query"):
                # self.poutput("prepend query hook")
                self.register_command_set(self._query)
            elif command == "answer" or rest_args.startswith("answer"):
                # self.poutput("prepend answer hook")
                self.register_command_set(self._answer)
        except CommandSetRegistrationError:
            pass  # command already registered
        if not command.startswith("padns"):
            command = f"padns {command}"
            new_command = f'{command} {rest_args} {post_command}'
            if not self.prompt == "SP (PADNS)# ":
                self.pwarning(f"Rewriting as: '{new_command}'")
            data.statement = self.statement_parser.parse(new_command)
        return data

    def _add_ioc_to_cache(self, ioc: str) -> None:
        if ioc not in self._ioc_cache:
            self._ioc_cache.append(ioc)

    def _get_iocs_from_history(self) -> List[str]:
        return [
            h.statement.args for h in self.history if h.statement.command in ["enrich", ]
        ]

    def do_intro(self, _):
        """Display the intro banner"""
        self.poutput(self.intro)

    load_parser = cmd2.Cmd2ArgumentParser()
    load_parser.add_argument('cmds', choices=['padns'])  #'query', 'answer'])

    @with_argparser(load_parser)
    @with_category('Command Loading')
    def do_load(self, ns: argparse.Namespace):
        # self.poutput(f"ns: {ns}")
        if ns.cmds == 'padns':
            self.prompt = "SP (PADNS)# "
            try:
                self.register_command_set(self._query)
                self.register_command_set(self._answer)
                self.poutput('PADNS loaded')
            except (ValueError, CommandSetRegistrationError) as e:
                self.poutput('PADNS already loaded')
                # self.perror(e)
        # if ns.cmds == 'query':
        #     try:
        #         self.register_command_set(self._query)
        #         self.prompt = "SP (PADNS/Query)# "
        #         self.poutput('PADNS/Query loaded')
        #     except (ValueError, CommandSetRegistrationError) as e:
        #         self.poutput('PADNS/Query already loaded')
        #         # self.perror(e)
        # if ns.cmds == 'answer':
        #     try:
        #         self.register_command_set(self._answer)
        #         self.prompt = "SP (PADNS/Answer)# "
        #         self.poutput('PADNS/Answer loaded')
        #     except (ValueError, CommandSetRegistrationError) as e:
        #         self.poutput('PADNS/Answer already loaded')
        #         # self.perror(e)

    @with_argparser(load_parser)
    @with_category('Command Loading')
    def do_unload(self, ns: argparse.Namespace):
        if ns.cmds == 'padns':
            self.prompt = "SP# "
            self.unregister_command_set(self._query)
            self.unregister_command_set(self._answer)
            self.poutput('PADNS unloaded')
        # if ns.cmds == 'query':
        #     self.unregister_command_set(self._query)
        #     self.poutput('PADNS/Query unloaded')
        # if ns.cmds == 'answer':
        #     self.unregister_command_set(self._answer)
        #     self.poutput('PADNS/Answer unloaded')

    padns_parser = cmd2.Cmd2ArgumentParser()
    padns_parser.add_subparsers(
        title='PADNS command',
        help='query/answer or any PADNS available command'
    )

    @with_argparser(padns_parser)
    def do_padns(self, ns: argparse.Namespace):
        # Call handler for whatever subcommand was selected
        handler = ns.cmd2_handler.get()
        if handler is not None:
            try:
                handler(ns)
            except TypeError as e:
                # self.perror(e)
                self.do_help('padns')
        else:
            # No subcommand was provided, so call help
            self.poutput('This command does nothing without sub-parsers registered')
            self.do_help('padns')


def main(argv=None):
    app_man = AppFileManager(__app_name__)
    app_man.create_hist_dir()  # Create history and cache directories
    app = App(application_manager=app_man)
    parser = argparse.ArgumentParser(prog="SP-CLI")
    command_help = 'command: score/enrich/query/answer (if none, enter interactive shell)'
    parser.add_argument("command", nargs='?', help=command_help)
    arg_help = 'optional arguments for command: -j/-c/-t'
    parser.add_argument('command_args', nargs=argparse.REMAINDER, help=arg_help)
    args = parser.parse_args(argv)
    exit_code = 0
    if args.command:
        app.onecmd_plus_hooks('{} {}'.format(args.command, ' '.join(args.command_args)))
    else:
        exit_code = app.cmdloop()
    return exit_code


if __name__ == '__main__':
    import sys

    sys.exit(main())

# @TODO:
# save command,
# config file,
# batch commands (sp < file),
# daemon, -o (to save output),
# fields list only (name, total, risk_score...)

# pyinstaller --paths=. --hidden-import commands sp.py
