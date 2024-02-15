#!/usr/bin/env python3
# coding=utf-8
import argparse
from typing import List

from cmd2 import with_category, Cmd

__app_name__ = "SP-CLI"

from common.utils import AppFileManager
from commands import *


class App(Cmd):

    intro = "Silent Push - CLI"
    prompt = "SP# "


    def __init__(self, **kwargs):
        self.app_man = kwargs.get("application_manager")
        hist_file = self.app_man.hist_file
        super().__init__(
            persistent_history_file=hist_file,
            persistent_history_length=500,
            allow_cli_args=False
        )
        # Create a cache object to save url information to
        self._ioc_cache: List = self._get_iocs_from_history()

    def _get_iocs_from_history(self) -> List[str]:
        return [
            h.statement.args for h in self.history if h.statement.command in ["enrich", ]
        ]

    def do_intro(self, _):
        """Display the intro banner"""
        self.poutput(self.intro)


def main():
    app_man = AppFileManager(__app_name__)
    app_man.create_hist_dir()  # Create history and cache directories
    app = App(application_manager=app_man)
    parser = argparse.ArgumentParser(prog="SP-CLI")
    parser.add_argument("command", nargs='*')
    args = parser.parse_args()
    exit_code = 0
    if args.command:
        app.onecmd_plus_hooks(' '.join(args.command))
    else:
        exit_code = app.cmdloop()
    return exit_code


if __name__ == '__main__':
    import sys
    sys.exit(main())