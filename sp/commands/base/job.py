import json

import requests

from sp.commands.base.BaseCommand import BaseCommand
from sp.common.utils import encode_path_segment
from sp.settings import API_KEY, API_URL


class Job(BaseCommand):
    """
    Job status command: used when long running tasks return a job ID
    """

    _URL = API_URL + "v1/explore/job/{job_id}/"
    """The job status endpoint URL"""

    def __enter__(self):
        """
        The logic before executing the command

        :return: Job
        """
        self._URL = self._URL.format(job_id=encode_path_segment(self._params.job_id))
        super().__enter__()
        return self

    def status(self):
        """
        The command main logic

        :return: None
        """
        self._response = requests.get(self._URL, headers={"x-api-key": API_KEY})
        if self.check_response():
            return
        try:
            self._response = json.loads(self._response.content)
        except json.JSONDecodeError as e:
            self._commandSet._cmd.perror(f"Can't parse command response: {e.msg}")
