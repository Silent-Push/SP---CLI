import functools
from typing import Any

import cmd2
from cmd2 import CommandSetRegistrationError, Fg, style

from sp.common.exceptions import CommandError
from sp.settings import MULTILINE_COMMANDS, get_initial_commands


class BaseCmdApp(cmd2.Cmd):
    """
    The cmd2 base class, handles the main logic needed by all commands
    """

    intro: str = "Silent Push - CLI"
    """The intro banner for the interactive mode"""
    prompt = style("SP# ", fg=Fg[Fg.LIGHT_GRAY.name.upper()], bold=True)
    """The prompt"""
    PREPEND_COMMANDS: list = [
        "padns",
        "query",
        "answer",
    ]
    """The list of sub commands that should be prepended with their main commands"""
    LOADED_COMMAND: str = ""
    """The loaded main command that should be displayed in the prompt"""

    def __init__(self, **kwargs):
        self.app_man = kwargs.get("application_manager")
        hist_file = self.app_man.hist_file
        super().__init__(
            persistent_history_file=hist_file,
            persistent_history_length=500,
            command_sets=get_initial_commands(),
            auto_load_commands=False,
            allow_cli_args=False,  # we use our own argparse,
            multiline_commands=MULTILINE_COMMANDS,
            shortcuts={},
        )
        self.foreground_color = Fg.CYAN.name.lower()
        # Create a cache object to save url information to
        self._ioc_cache: list = self._get_iocs_from_history()
        self.register_postparsing_hook(self.prepend_padns_main_command_hook)

    def perror(self, *args, **kwargs) -> None:
        """
        Overrides cmd2.Cmd.perror: prints the error and, when running a single command like `score x.ie`, exit with 1
        so shell scripts can detect the failure

        :return: None
        """
        if not getattr(self, "interactive", False):
            self.exit_code = 1
        super().perror(*args, **kwargs)

    def pwarning(self, msg: Any = "", *, end: str = "\n") -> None:
        """
        Overrides cmd2.Cmd.pwarning: cmd2 prints warnings through perror, a warning isn't a failure
        so it skips our perror and keeps the exit code

        :param msg: The warning to print
        :param end: The string appended after the message
        :return: None
        """
        super().perror(cmd2.ansi.style_warning(msg), end=end, apply_style=False)

    def pexcept(self, msg, *args, **kwargs) -> None:
        """
        Overrides cmd2.Cmd.pexcept: cmd2 calls it for any exception raised by a command,
        it's what stops a command with a CommandError

        :param msg: The exception
        :return: None
        """
        if isinstance(msg, CommandError):
            msg.show(self)
            return
        super().pexcept(msg, *args, **kwargs)

    def prepend_padns_main_command_hook(
            self, data: cmd2.plugin.PostparsingData
    ) -> cmd2.plugin.PostparsingData:
        """
        A post parsing hook to automatically precede sub commands
        so user can type like 'query a...' rather than 'padns query a...'

        :param data: The original post parsing object within the command and arguments
        :return: The modified post parsing object
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
                from sp.commands.answer import PADNSAnswerCommandSet
                from sp.commands.query import PADNSQueryCommandSet

                self._query = PADNSQueryCommandSet()
                self._answer = PADNSAnswerCommandSet()
                self.register_command_set(self._query)
                self.register_command_set(self._answer)
            elif command == "query" or rest_args.startswith("query"):
                from sp.commands.query import PADNSQueryCommandSet

                self._query = PADNSQueryCommandSet()
                # self.poutput("prepend query hook")
                command = f"padns {command}"
                self.register_command_set(self._query)
            elif command == "answer" or rest_args.startswith("answer"):
                from sp.commands.answer import PADNSAnswerCommandSet

                self._answer = PADNSAnswerCommandSet()
                # self.poutput("prepend answer hook")
                command = f"padns {command}"
                self.register_command_set(self._answer)
        except CommandSetRegistrationError:
            pass  # command already registered
        new_command = f"{command} {rest_args} {post_command}"
        # if not self.LOADED_COMMAND == "padns":
        #     self.pwarning(f"Rewriting as: '{new_command}'")
        data.statement = self.statement_parser.parse(new_command)
        return data

    @functools.singledispatchmethod
    def _add_ioc_to_cache(self, ioc: str) -> None:
        """
        Adds IoCs to cache, so they can be part of the command history and
        be offered as choices to commands that need IoC

        :param ioc: The IoC to be added to cache
        :return: None
        """
        if ioc not in self._ioc_cache:
            self._ioc_cache.append(ioc)

    @_add_ioc_to_cache.register(list)
    def _(self, iocs: list):  # _add_ioc_to_cache overloaded method
        for ioc in iocs:
            self._add_ioc_to_cache(ioc)

    def _get_iocs_from_history(self) -> list[str]:
        """
        The initial IoCs history

        :return: The list of IoCs history
        """
        return [
            h.statement.args
            for h in self.history
            if h.statement.command in ["enrich", "score", "query", "answer"]
        ]

    def do_intro(self, _):
        """
        Displays the intro banner

        :param _:
        :return:
        """
        self.poutput(style(self.intro, fg=Fg[self.foreground_color.upper()]))
