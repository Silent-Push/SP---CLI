#!/usr/bin/env python3
# coding=utf-8

__app_name__ = "SP-CLI"

from cmd2 import CommandSetRegistrationError, Fg, style, with_category

from sp.commands import *
from sp.commands.base.BaseCmdApp import BaseCmdApp
from sp.common.utils import AppFileManager, categorize_subcommands
from sp.settings import SPQL_COMMANDS


class App(BaseCmdApp):
    """
    The core class which the CLI is instantiated
    """

    load_parser = cmd2.Cmd2ArgumentParser()
    """The argument parser for the load command"""
    load_parser.add_argument(
        "cmds",
        choices=[
            "padns",
        ],
    )

    @with_argparser(load_parser)
    @with_category("Command Loading")
    def do_load(self, ns: argparse.Namespace):
        """
        Switches to a command group and loads it's sub commands i.e.: padns

        :param ns: The argument passed to the load command
        :return: None
        """
        # self.poutput(f"ns: {ns}")
        if ns.cmds == "padns":
            self.prompt = style(
                "SP (PADNS)# ", fg=Fg[Fg.LIGHT_GRAY.name.upper()], bold=True
            )
            self.LOADED_COMMAND = "padns"
            try:
                from sp.commands.query import PADNSQueryCommandSet
                from sp.commands.answer import PADNSAnswerCommandSet
                from sp.commands.search import PADNSSearchCommandSet

                self._query = PADNSQueryCommandSet()
                self._answer = PADNSAnswerCommandSet()
                self._search = PADNSSearchCommandSet()
                self.register_command_set(self._query)
                self.register_command_set(self._answer)
                self.register_command_set(self._search)
                categorize_subcommands("PADNS Query", self, PADNSQueryCommandSet)
                categorize_subcommands("PADNS Answer", self, PADNSAnswerCommandSet)
                categorize_subcommands("PADNS Search", self, PADNSSearchCommandSet)
                self.poutput("PADNS loaded")
            except (ValueError, CommandSetRegistrationError) as e:
                self.poutput("PADNS already loaded")

    @with_argparser(load_parser)
    @with_category("Command Loading")
    def do_unload(self, ns: argparse.Namespace):
        """
        Switches off the loaded command group and return to single prompt

        :param ns: The argument passed to the unload command
        :return: None
        """
        if ns.cmds == "padns":
            self.prompt = style("SP# ", fg=Fg[Fg.LIGHT_GRAY.name.upper()], bold=True)
            self.unregister_command_set(self._query)
            self.unregister_command_set(self._answer)
            self.LOADED_COMMAND = ""
            self.poutput("PADNS unloaded")

    padns_parser = cmd2.Cmd2ArgumentParser()
    """The argument parser for the padns command"""
    padns_parser.add_subparsers(
        title="PADNS command", help="query/answer or any PADNS available command"
    )

    # @with_category("PADNS")
    @with_argparser(padns_parser)
    def do_padns(self, ns: argparse.Namespace):
        """
        The PADNS main command

        :param ns: The padns sub command i.e.: query
        :return: None
        """
        # Call handler for whatever subcommand was selected
        handler = ns.cmd2_handler.get()
        if handler is not None:
            try:
                handler(ns)
            except TypeError:
                # self.perror(e)
                handler("")
        else:
            # No subcommand was provided, so call help
            self.do_help("padns")


def main(argv=None):
    """
    Instantiate the CLI app and handles the prompt including interactive

    :param argv: The initial command passed
    :return: The exit code to the OS
    """
    app_man = AppFileManager(__app_name__)
    app_man.create_hist_dir()  # Create history and cache directories
    app = App(application_manager=app_man)
    parser = argparse.ArgumentParser(prog="sp")
    command_help = "command: score/enrich/padns (if none, enter interactive shell)"
    parser.add_argument("command", nargs="?", help=command_help)
    arg_help = "optional arguments for command: -j/-c/-t"
    parser.add_argument("command_args", nargs=argparse.REMAINDER, help=arg_help)
    args = parser.parse_args(argv)
    exit_code = 0
    if args.command:
        app.interactive = False
        if args.command in SPQL_COMMANDS:
            if (
                    args.command_args[0].find('"') == -1
                    and args.command_args[0].find("'") == -1
            ):
                args.command_args[0] = f'"{args.command_args[0]}"'
            elif args.command_args[0].find('"') >= 0:
                args.command_args[0] = f"'{args.command_args[0]}'"
            elif args.command_args[0].find("'") >= 0:
                app.pwarning("Please use double quotes with SPQL!")
                args.command_args[0] = f'"{args.command_args[0]}"'
        new_args = " ".join(args.command_args)
        app.onecmd_plus_hooks("{} {}".format(args.command, new_args))
    else:
        app.interactive = True
        exit_code = app.cmdloop()
    return exit_code


if __name__ == "__main__":
    import sys

    sys.exit(main())

# @TODO: verbose, version
