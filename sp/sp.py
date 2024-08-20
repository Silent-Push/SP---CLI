#!/usr/bin/env python3
# coding=utf-8

__app_name__ = "SP-CLI"

from cmd2 import with_category, CommandSetRegistrationError, style, Fg

from sp.commands.base.BaseCmdApp import BaseCmdApp
from sp.common.utils import AppFileManager
from sp.commands import *


class App(BaseCmdApp):

    load_parser = cmd2.Cmd2ArgumentParser()
    load_parser.add_argument("cmds", choices=["padns"])  # 'query', 'answer'])

    @with_argparser(load_parser)
    @with_category("Command Loading")
    def do_load(self, ns: argparse.Namespace):
        # self.poutput(f"ns: {ns}")
        if ns.cmds == "padns":
            self.prompt = style(
                "SP (PADNS)# ", fg=Fg[Fg.LIGHT_GRAY.name.upper()], bold=True
            )
            self.LOADED_COMMAND = "padns"
            try:
                self.register_command_set(self._query)
                self.register_command_set(self._answer)
                self.poutput("PADNS loaded")
            except (ValueError, CommandSetRegistrationError):
                self.poutput("PADNS already loaded")

    @with_argparser(load_parser)
    @with_category("Command Loading")
    def do_unload(self, ns: argparse.Namespace):
        if ns.cmds == "padns":
            self.prompt = style("SP# ", fg=Fg[Fg.LIGHT_GRAY.name.upper()], bold=True)
            self.unregister_command_set(self._query)
            self.unregister_command_set(self._answer)
            self.LOADED_COMMAND = ""
            self.poutput("PADNS unloaded")

    padns_parser = cmd2.Cmd2ArgumentParser()
    padns_parser.add_subparsers(
        title="PADNS command", help="query/answer or any PADNS available command"
    )

    @with_category("PADNS")
    @with_argparser(padns_parser)
    def do_padns(self, ns: argparse.Namespace):
        # Call handler for whatever subcommand was selected
        handler = ns.cmd2_handler.get()
        if handler is not None:
            try:
                handler(ns)
            except TypeError:
                # self.perror(e)
                self.do_help("padns")
        else:
            # No subcommand was provided, so call help
            self.do_help("padns")


def main(argv=None):
    app_man = AppFileManager(__app_name__)
    app_man.create_hist_dir()  # Create history and cache directories
    app = App(application_manager=app_man)
    parser = argparse.ArgumentParser(prog="SP-CLI")
    command_help = "command: score/enrich/padns (if none, enter interactive shell)"
    parser.add_argument("command", nargs="?", help=command_help)
    arg_help = "optional arguments for command: -j/-c/-t"
    parser.add_argument("command_args", nargs=argparse.REMAINDER, help=arg_help)
    args = parser.parse_args(argv)
    exit_code = 0
    if args.command:
        app.onecmd_plus_hooks("{} {}".format(args.command, " ".join(args.command_args)))
    else:
        exit_code = app.cmdloop()
    return exit_code


if __name__ == "__main__":
    import sys

    sys.exit(main())
