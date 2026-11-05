from cmd2 import Statement, with_argparser, with_default_category

from sp.commands.base.BaseCommand import BaseCommand
from sp.commands.base.BaseCommandSet import BaseCommandSet
from sp.common.exceptions import ResponseParseError
from sp.common.parse_ioc import IOCUtils
from sp.common.utils import encode_path_segment
from sp.settings import API_URL


# @TODO: rename to riskscore
@with_default_category("Scoring")
class ScoreCommandSet(BaseCommandSet):
    """
    The Score Command Set
    """

    _score_parser = BaseCommandSet._get_score_arg_parser()
    """The argument parser for the score command"""

    @with_argparser(_score_parser)
    def do_score(self, params: Statement):
        """
        Scores a domain, IP or URL

        :param params: The passed command parameters
        :return: None
        """
        # @TODO: maybe move this to parent class to avoid repetition
        if not IOCUtils(params.ioc).valid:
            self._cmd.perror("Not a valid IoC")
            return
        with self.Score(params, self) as scoring:
            scoring.score()

    class Score(BaseCommand):
        """
        The Score command, it's a context manager class
        """

        _URL = API_URL + "v1/explore/{type}/riskscore/{ioc}/?format=json"
        """The score endpoint URL"""

        def __enter__(self):
            """
            Overrides BaseCommand.__enter__: the logic before executing the command

            :return: Score
            """
            self.ioc_type = IOCUtils(self._params.ioc).type
            self._URL = self._URL.format(
                type=self.ioc_type, ioc=encode_path_segment(self._params.ioc)
            )
            super().__enter__()
            return self

        def score(self):
            """
            The command main logic

            :return: None
            """
            response = self.call_api().get("response")
            if self._params.verbose:
                self._result = response
                return
            try:
                if self.ioc_type == "domain":
                    self._result = response.get("sp_risk_score")
                else:
                    self._result = response.get("ip2asn")[0].get("sp_risk_score")
            except (IndexError, TypeError, AttributeError) as e:
                raise ResponseParseError(e)

        def __exit__(self, exc_type, exc_val, exc_tb):
            """
            Overrides BaseCommand.__exit__: the logic after executing the command

            :param exc_type: Exception type, if need to catch
            :param exc_val: Exception value
            :param exc_tb: Exception traceback
            :return: None
            """
            super().__exit__(exc_type, exc_val, exc_tb)
            self._commandSet._cmd._add_ioc_to_cache(self._params.ioc)
