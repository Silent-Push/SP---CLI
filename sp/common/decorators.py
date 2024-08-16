import functools
import os

from sp.common.parse_ioc import IOCUtils
from sp.common.utils import strip_command_options


def validate_ioc(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        command_set, *statement = args
        try:
            ioc = strip_command_options(command_set, statement[0])
            if ioc:
                if not IOCUtils(ioc).validate():
                    command_set._cmd.perror("Not a valid IoC")
                    return
        except AttributeError:
            pass
        return func(*args, **kwargs)

    return wrapper


def targeted_command(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        command_set, *statement = args
        ioc = strip_command_options(command_set, statement[0])
        if not ioc:
            if os.environ.get("_sp_target"):
                list_args = list(args)
                list_args[1] = os.environ.get("_sp_target") + " " + list_args[1]
                args = tuple(list_args)
            else:
                command_set._cmd.perror(
                    "Not a valid IoC, try the command 'target <your_ioc>'"
                )
                return
        return func(*args, **kwargs)

    return wrapper
