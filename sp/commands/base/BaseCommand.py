import json

import pandas
from cmd2 import CommandSet, Statement
from cmd2.ansi import style_success

from sp import settings
from sp.common.utils import (
    PandasDataFrameTSV, encode_query_params, flatten_dict, flatten_list,
)
from sp.settings import CRLF


class BaseCommand:
    """
    Contains all common methods used for all Command classes
    """

    _commandSet: CommandSet = None
    """The CommandSet object passed by the child class"""
    _response: dict = {}
    """The API response"""
    _params: Statement = None
    """The Statement object passed by the child class"""
    _output: str = ""
    """The final command result output"""

    def __init__(self, params: Statement, command_set: CommandSet):
        """
        Context manager base class for all commands

        >>> with BaseCommand(statement, command_set) as command:
        ...    command.do_something()

        :param params: The passed command options
        :param command_set: The CommandSet object related to the command
        """
        if not settings.API_KEY:
            raise EnvironmentError(settings.MISSING_API_KEY_MESSAGE)
        self._commandSet = command_set
        self._params = params

    def __enter__(self):
        """
        Override this method if you need anything done before executing the command

        >>> def __enter__(self):
        ...     print("loading command...")
        ...     return super().__enter__()

        :return: BaseCommand
        """
        if hasattr(self._params, "params") and self._params.params:
            self._URL += "&" + encode_query_params(self._params.params)
        # self._commandSet._cmd.poutput(self._URL)
        # self._commandSet._cmd.pfeedback(f"\t{self._feedback}...")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Override this method if you need anything done after executing the command

        >>> def __exit__(self):
        ...     print("command done!")
        ...     return super().__exit__()

        :param exc_type:
        :param exc_val:
        :param exc_tb:
        :return: None
        """
        if self._response is None:
            return
        flattened = self._response
        if isinstance(self._response, dict):
            flattened = flatten_dict(self._response)
        elif isinstance(self._response, list):
            flattened = flatten_list(self._response)
        if self._params.json:
            self._output = json.dumps(self._response, indent=2) + CRLF
        elif self._params.csv:
            try:
                dataframe = pandas.DataFrame(flattened, index=[0])
                dataframe = dataframe.transpose()
                self._output = dataframe.to_csv(header=False) + CRLF
            except ValueError:
                self._output = flattened
        elif self._params.tsv:
            try:
                dataframe = PandasDataFrameTSV(flattened, index=[0])
                self._output = dataframe.to_tsv() + CRLF
            except ValueError:
                self._output = flattened
        else:
            try:
                self._output = json.dumps(self._response, indent=2) + CRLF
            except TypeError:
                self._commandSet._cmd.perror(
                    "Something went wrong, wrong syntax? Try 'help <command>'"
                )
        self._commandSet._cmd.poutput(style_success(self._output))
        # used by the run_script and run_pyscript command
        self._commandSet._cmd.last_result = self._output
        # self._commandSet._cmd.pfeedback(f"\t*{self._feedback}")

    def check_response(self) -> bool:
        """
        Checks the API response for errors or long running jobs, call it right after the request

        >>> if self.check_response():
        ...     return

        :return: True if the command should stop, there are no results to parse
        """
        if self.check_error():
            self._response = None
            return True
        return self.check_job()

    def check_job(self) -> bool:
        """
        Long running tasks return a job instead of the result, warns how to get it later with the job command

        :return: True if the response is a job, so the command can stop parsing it
        """
        try:
            content = json.loads(self._response.content)
        except (json.JSONDecodeError, AttributeError, TypeError):
            return False
        if not isinstance(content, dict):
            return False
        # newer endpoints return the job at the top level, older ones wrap it in "response"
        response = content.get("response")
        job_status = content.get("job_status") or (response.get("job_status") if isinstance(response, dict) else None)
        if not job_status:
            return False
        self._commandSet._cmd.pwarning(
            f"This command is taking too long, try again later using the command: `job {job_status.get('job_id')}`"
        )
        self._response = job_status
        return True

    def check_error(self) -> bool:
        """
        Tries to extract as much error from the response payload as possible

        :return: True if the API returned an error
        """
        if not self._response.status_code == 200:
            import json
            import re

            # try to extract the error from the API response
            content = self._response.content.decode()
            try:
                json_error = json.loads(content).get("errors")
            except (json.JSONDecodeError, TypeError):
                json_error = ""
            strip = re.compile("<.*?>|\n")
            error = re.sub(strip, " ", content[content.find("<body"):])
            error = re.sub(' +', ' ', error)
            error += json_error.__str__()
            self._commandSet._cmd.perror("Something went wrong :(")
            self._commandSet._cmd.perror(
                f"Status Code {self._response.status_code}: {error[:100]}..."
            )
            self._commandSet._cmd.pwarning("Is your API key correct?")
            return True
        return False
