from typing import List

from cmd2 import CommandSetRegistrationError, Fg, style

from sp.commands import (
    PADNSQueryCommandSet,
    PADNSAnswerCommandSet,
    EnrichCommandSet,
    ScoreCommandSet,
)

import cmd2


class BaseCmdApp(cmd2.Cmd):
    intro = "Silent Push - CLI"
    prompt = style("SP# ", fg=Fg[Fg.LIGHT_GRAY.name.upper()], bold=True)
    PREPEND_COMMANDS = ["padns", "query", "answer"]
    LOADED_COMMAND = ""

    def __init__(self, **kwargs):
        self.app_man = kwargs.get("application_manager")
        hist_file = self.app_man.hist_file
        super().__init__(
            persistent_history_file=hist_file,
            persistent_history_length=500,
            auto_load_commands=False,
            allow_cli_args=False,  # we use our own argparse,
        )
        self.foreground_color = Fg.CYAN.name.lower()
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
            new_command = f"{command} {rest_args} {post_command}"
            # if not self.LOADED_COMMAND == "padns":
            #     self.pwarning(f"Rewriting as: '{new_command}'")
            data.statement = self.statement_parser.parse(new_command)
        return data

    def _add_ioc_to_cache(self, ioc: str) -> None:
        if ioc not in self._ioc_cache:
            self._ioc_cache.append(ioc)

    def _get_iocs_from_history(self) -> List[str]:
        return [
            h.statement.args
            for h in self.history
            if h.statement.command
            in [
                "enrich",
            ]
        ]

    def do_intro(self, _):
        """Display the intro banner"""
        self.poutput(style(self.intro, fg=Fg[self.foreground_color.upper()]))
