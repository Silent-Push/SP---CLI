import json
import requests

from cmd2 import (
    Statement,
    with_argparser,
    with_default_category,
)

from common.BaseCommand import BaseCommand
from common.BaseCommandSet import BaseCommandSet
from common.parse_ioc import IOCUtils
from settings import CRLF, API_URL, API_KEY


@with_default_category("Scoring")
class ScoreCommandSet(BaseCommandSet):

    _score_parser = BaseCommandSet._get_arg_parser()
    _score_parser.add_argument(
        "ioc",
        choices_provider=(lambda self: self._cmd._ioc_cache),
        help="IoC to score"
    )

    @with_argparser(_score_parser)
    def do_score(self, params: Statement):
        if not IOCUtils(params.ioc).validate():
            self._cmd.perror("Not a valid IoC")
            return
        with self.Scoring(params, self) as scoring:
            scoring.score()

    class Scoring(BaseCommand):
        __URL = API_URL + "explore/{type}/riskscore/{ioc}/"

        def __enter__(self):
            self.__URL = self.__URL.format(
                type=IOCUtils(self._params.ioc).type,
                ioc=self._params.ioc
            )
            return self

        def score(self):
            response = requests.get(
                self.__URL,
                headers={"x-api-key": API_KEY}
            )
            self._response = json.loads(response.content).get("response")

        def __exit__(self, exc_type, exc_val, exc_tb):
            super().__exit__(exc_type, exc_val, exc_tb)
            self._commandSet._cmd.poutput(self._output)
            self._commandSet._cmd._add_ioc_to_cache(self._params.ioc)
