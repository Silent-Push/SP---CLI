import os

from cmd2 import (
    Statement,
    with_argparser,
    with_default_category,
    Cmd2ArgumentParser,
)

from sp.commands.base.BaseCommandSet import BaseCommandSet
from sp.common.parse_ioc import IOCUtils


# @TODO: WIP
@with_default_category("Target Context")
class TargetContextCommandSet(BaseCommandSet):

    _target_parser = Cmd2ArgumentParser()
    _target_parser.add_argument(
        "ioc", help="Type an IP, Domain or URL to set the target of next commands"
    )

    @with_argparser(_target_parser)
    def do_target(self, params: Statement):
        """
        Set the target of next commands
        """
        if not IOCUtils(params.ioc).validate():
            self._cmd.perror("Not a valid IoC")
            return
        os.environ.setdefault("_sp_target", params.ioc)
        self._cmd.prompt = f"SP ({params.ioc})# "
        self._cmd.pfeedback(
            "\tYou can now type any command without the IoC, i.e.: 'query ns'"
        )
