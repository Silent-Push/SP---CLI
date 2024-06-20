import json

import pandas

from sp.common.utils import flatten_dict, PandasDataFrameTSV
from sp.settings import CRLF


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
            self._URL += "&" + "&".join(self._params.params)
        # self._commandSet._cmd.poutput(self._URL)
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

    def check_error(self):
        if not self._response.status_code == 200:
            import re
            import json

            # try to extract the error from the API response
            content = self._response.content.decode()
            try:
                json_error = json.loads(content).get("errors")
            except (json.JSONDecodeError, TypeError):
                json_error = ''
            strip = re.compile('<.*?>|\n')
            error = re.sub(strip, '', content[content.find('<body'):])
            error += json_error.__str__()
            self._commandSet._cmd.perror("Something went wrong :(")
            self._commandSet._cmd.perror(
                f"Status Code {self._response.status_code}: "
                f"{error[:100]}..."
            )
            self._commandSet._cmd.pwarning("Is your API key correct?")
            return

