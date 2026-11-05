from typing import Any

from sp.commands.base.BaseCommand import BaseCommand
from sp.common.utils import encode_path_segment
from sp.settings import API_URL


class Job(BaseCommand):
    """
    Job status command: used when long running tasks return a job ID
    """

    _URL = API_URL + "v1/explore/job/{job_id}/"
    """The job status endpoint URL"""

    def __enter__(self):
        """
        Overrides BaseCommand.__enter__: the logic before executing the command

        :return: Job
        """
        self._URL = self._URL.format(job_id=encode_path_segment(self._params.job_id))
        super().__enter__()
        return self

    def get_job_id(self, content: Any) -> None:
        """
        Overrides BaseCommand.get_job_id: the job command doesn't need it

        :param content: The parsed JSON response
        :return: None, never stops the job command
        """
        return None

    def status(self):
        """
        The command main logic

        :return: None
        """
        self._result = self.call_api()
