from cmd2 import Statement, with_argparser, with_default_category

from sp.commands.base.BaseCommandSet import BaseCommandSet
from sp.commands.base.job import Job


@with_default_category("Utils")
class JobCommandSet(BaseCommandSet):
    job_parser = BaseCommandSet._get_job_arg_parser()
    """The argument parser for the job command"""

    @with_argparser(job_parser)
    def do_job(self, params: Statement):
        """
        Get the job status of a running long task

        :param params: The passed command parameters
        :return: None
        """
        with Job(params, self) as job:
            job.status()
