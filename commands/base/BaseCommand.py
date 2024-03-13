import json

import pandas

from common.utils import flatten_dict, PandasDataFrameTSV
from settings import CRLF


class BaseCommand:
    _commandSet = None
    _response = {}
    _params = None
    _output = ""

    def __init__(self, params, command_set):
        self._commandSet = command_set
        self._params = params

    def __enter__(self):
        if self._params.params:
            self._URL += "?" + "&".join(self._params.params)
        self._commandSet._cmd.pfeedback(f"\t{self._feedback}...")

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._params.json:
            self._output = json.dumps(self._response, indent=2) + CRLF
        elif self._params.csv:
            dataframe = pandas.DataFrame(
                flatten_dict(self._response),
                index=[0]
            )
            dataframe = dataframe.transpose()
            self._output = dataframe.to_csv() + CRLF
        elif self._params.tsv:
            dataframe = PandasDataFrameTSV(
                flatten_dict(self._response),
                index=[0]
            )
            self._output = dataframe.to_tsv() + CRLF
        else:
            self._output = json.dumps(self._response, indent=2) + CRLF
        self._commandSet._cmd.poutput(self._output)
        # used by the run_script and run_pyscript command
        self._commandSet._cmd.last_result = self._output
        self._commandSet._cmd.pfeedback(f"\t*{self._feedback}")

