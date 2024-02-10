from pathlib import Path

from xdg import XDG_CACHE_HOME, XDG_DATA_HOME


class AppFileManager:
    """Application file manager used to abstract location and usage of persistent history file."""

    def __init__(self, app_name: str):
        self.app_name = app_name
        self._hist_file = XDG_DATA_HOME.joinpath(self.app_name, "persistent_history.cmd2")

    @property
    def hist_file(self) -> Path:
        return self._hist_file

    def create_hist_dir(self) -> Path:
        XDG_DATA_HOME.joinpath(self.app_name).mkdir(parents=True, exist_ok=True)
