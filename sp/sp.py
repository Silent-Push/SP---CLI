#!/usr/bin/env python3
# coding=utf-8
import argparse
import cmd2
from typing import List

__app_name__ = "SP-CLI"

from sp.common.utils import AppFileManager
from sp.commands import *


class App(cmd2.Cmd):

    intro = "Silent Push - CLI"
    prompt = "SP# "


    def __init__(self, **kwargs):
        self.app_man = kwargs.get("application_manager")
        hist_file = self.app_man.hist_file
        super().__init__(
            persistent_history_file=hist_file,
            persistent_history_length=500,
            allow_cli_args=False  # we use our own argparse
        )
        # Create a cache object to save url information to
        self._ioc_cache: List = self._get_iocs_from_history()

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

# @TODO: save command, config file, batch commands (sp < file), daemon, -o (to save output)

# pyinstaller --paths=. --hidden-import commands sp.py