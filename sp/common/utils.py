from pathlib import Path
from typing import Callable

import cmd2
import pandas
from pandas import DataFrame
from xdg import XDG_DATA_HOME


class AppFileManager:
    """
    Application file manager used to abstract location and usage of
    persistent history file.
    """

    def __init__(self, app_name: str):
        self.app_name = app_name
        self._hist_file = XDG_DATA_HOME.joinpath(
            self.app_name, "persistent_history.cmd2"
        )

    @property
    def hist_file(self) -> Path:
        return self._hist_file

    def create_hist_dir(self) -> Path:
        XDG_DATA_HOME.joinpath(self.app_name).mkdir(parents=True, exist_ok=True)


class PandasDataFrameTSV(pandas.DataFrame):
    def to_tsv(self, *args, **kwargs) -> str:
        return self.transpose().to_string(max_colwidth=200, header=False)

    @property
    def _constructor(self) -> Callable[..., DataFrame]:
        return PandasDataFrameTSV


def categorize_subcommands(category: str, app: cmd2.Cmd, command_set: cmd2.CommandSet):
    """
    Categorize subcommands without the unnecessary extra underscores, so that
    the help will show the complete command with subcommand, example:
        given the command: do_a_b_c
        replaces with : a b c

    :param category: The string category
    :param app: The app which category to be added
    :param command_set: The command set to add commands to category
    :return:
    """
    import inspect
    from cmd2.constants import COMMAND_FUNC_PREFIX, HELP_FUNC_PREFIX

    methods = inspect.getmembers(
        command_set,
        predicate=lambda meth: inspect.isfunction(meth)
                               and meth.__name__.startswith(COMMAND_FUNC_PREFIX)
                               and meth in inspect.getmro(command_set)[0].__dict__.values(),
    )
    for method in methods:
        func_name, func_ = method
        command_suffix = " ".join(func_name.split("_")[1:])
        # Add command function to CLI object
        cmd_func_name = COMMAND_FUNC_PREFIX + command_suffix
        setattr(app, cmd_func_name, func_)
        # Add help function to CLI object
        help_func = lambda: app.poutput(func_.__doc__)
        help_func_name = HELP_FUNC_PREFIX + command_suffix
        setattr(app, help_func_name, help_func)
        delattr(app, func_name)  # delete old method do_a_b_c()
        cmd2.categorize(getattr(app, cmd_func_name), category)


def strip_command_options(command_set, args):
    for action in command_set._get_arg_parser()._get_optional_actions():
        for option in action.option_strings:
            args = args.strip(option)
    return args.strip()


def flatten_list(data):
    merged_list = dict()
    prefix = 0
    for d in data:
        if not isinstance(d, dict):
            return data
        merged_list = {**merged_list, **flatten_dict(d, str(f"{prefix}_"))}
        prefix += 1
    return merged_list


def flatten_dict(data, prefix=""):
    flatten_merged = {}
    merged_dict_keys = {}
    if not isinstance(data, dict):
        flatten_merged[f"{prefix}"] = data
        return flatten_merged
    for field, value in data.items():
        if isinstance(value, list):
            try:
                if isinstance(value[0], dict):
                    iterator = enumerate(value) if len(value) > 1 else value[0].items()
                    for _k, d in iterator:
                        if isinstance(d, dict):
                            merged_dict_keys = {
                                field + "_" + k + "_" + str(_k): v for k, v in d.items()
                            }
                        elif isinstance(d, str):
                            merged_dict_keys = {field + "_" + str(_k): d}
                        flatten_merged = {
                            **flatten_merged,
                            **flatten_dict(merged_dict_keys, prefix),
                        }
                    continue
                else:
                    value = ", ".join(str(v) for v in value)
            except IndexError:
                continue
        if isinstance(value, dict):
            merged_dict_keys = {field + "_" + k: v for k, v in value.items()}
            flatten_merged = {
                **flatten_merged,
                **flatten_dict(merged_dict_keys, prefix),
            }
            continue
        flatten_merged[f"{prefix}{field}"] = value
    return flatten_merged
