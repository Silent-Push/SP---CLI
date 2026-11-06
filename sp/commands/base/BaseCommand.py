import json
from typing import Any

import pandas
import requests
from cmd2 import CommandSet, Statement
from cmd2.ansi import style_success

from sp import settings
from sp.common.api import api
from sp.common.exceptions import (
    ApiConnectionError,
    ApiError,
    ApiTimeoutError,
    CommandError,
    JobPending,
    ResponseParseError,
)
from sp.common.utils import (
    PandasDataFrameTSV,
    encode_query_params,
    flatten_dict,
    flatten_list,
)
from sp.settings import CRLF


class BaseCommand:
    """
    Contains all common methods used for all Command classes
    """

    _commandSet: CommandSet = None
    """The CommandSet object passed by the child class"""
    _result: dict = {}
    """The command result, what __exit__ outputs"""
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
            raise CommandError(settings.MISSING_API_KEY_MESSAGE)
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
        if exc_type:  # the command failed, there's nothing to output
            return
        flattened = self._result
        if isinstance(self._result, dict):
            flattened = flatten_dict(self._result)
        elif isinstance(self._result, list):
            flattened = flatten_list(self._result)
        if self._params.json:
            self._output = json.dumps(self._result, indent=2) + CRLF
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
                self._output = json.dumps(self._result, indent=2) + CRLF
            except TypeError:
                self._commandSet._cmd.perror(
                    "Something went wrong, wrong syntax? Try 'help <command>'"
                )
        self._commandSet._cmd.poutput(style_success(self._output))
        # used by the run_script and run_pyscript command
        self._commandSet._cmd.last_result = self._output

    def call_api(self, method: str = "GET", payload: dict = None) -> Any:
        """
        Calls the command URL, the single entry point to the API for all commands

        :param method: GET or POST
        :param payload: The JSON body for POST requests
        :return: The parsed JSON response
        :raises CommandError: When there are no results, which stops the command
        """
        try:
            response = api.request(method, self._URL, payload)
        except requests.Timeout as e:
            raise ApiTimeoutError(settings.API_TIMEOUT) from e
        except requests.RequestException as e:
            raise ApiConnectionError(e) from e
        if response.status_code != 200:
            raise ApiError(response)
        try:
            content = json.loads(response.content)
        except json.JSONDecodeError as e:
            raise ResponseParseError(e) from e
        job_id = self.get_job_id(content)
        if job_id:
            raise JobPending(job_id)
        return content

    def get_job_id(self, content: Any) -> str | None:
        """
        Long running tasks return a job instead of the result

        :param content: The parsed JSON response
        :return: The job ID if the response is a job
        """
        if not isinstance(content, dict):
            return None
        # newer endpoints return the job at the top level, older ones wrap it in "response"
        response = content.get("response")
        job_status = content.get("job_status") or (response.get("job_status") if isinstance(response, dict) else None)
        return job_status.get("job_id") if job_status else None
