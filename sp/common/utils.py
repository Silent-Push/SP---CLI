from pathlib import Path
from typing import Callable

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
        return self.transpose().to_string()

    @property
    def _constructor(self) -> Callable[..., DataFrame]:
        return PandasDataFrameTSV


def strip_command_options(command_set, args):
    for action in command_set._get_arg_parser()._get_optional_actions():
        for option in action.option_strings:
            args = args.strip(option)
    return args.strip()


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
