import json
import pandas

from common.utils import flatten_dict
from settings import CRLF


class BaseCommand:
    _commandSet = None
    _response = {}
    _params = None
    _output = ""

    def __init__(self, params, command_set):
        self._commandSet = command_set
        self._params = params

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._output = json.dumps(self._response, indent=2) + CRLF
        if self._params.csv:
            dataframe = pandas.DataFrame(
                flatten_dict(self._response),
                index=[0]
            )
            dataframe = dataframe.transpose()
            self._output = dataframe.to_csv() + CRLF
