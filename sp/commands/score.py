import argparse
import json
import requests

from cmd2 import (
    Statement,
    with_argparser,
    with_default_category,
)

from sp.commands.base.BaseCommand import BaseCommand
from sp.commands.base.BaseCommandSet import BaseCommandSet
from sp.common.decorators import targeted_command, validate_ioc
from sp.common.parse_ioc import IOCUtils
from sp.settings import CRLF, API_URL, API_KEY


@with_default_category("Scoring")
class ScoreCommandSet(BaseCommandSet):

    _score_parser = BaseCommandSet._get_arg_parser()

    @targeted_command
    @validate_ioc
    @with_argparser(_score_parser)
    def do_score(self, params: Statement):
        """
        Scores a domain, IP or URL
        """
        with self.Scoring(params, self) as scoring:
            scoring.score()

    class Scoring(BaseCommand):
        _URL = API_URL + "explore/{type}/riskscore/{ioc}/?format=json"

        def __enter__(self):
            self._URL = self._URL.format(
                type=IOCUtils(self._params.ioc).type,
                ioc=self._params.ioc
            )
            self._feedback = f"{self._URL[self._URL.index('explore/') + 7:]}"
            super().__enter__()
            return self

        def score(self):
            self._response = requests.get(
                self._URL,
                headers={"x-api-key": API_KEY}
            )
            self.check_error()
            self._response = json.loads(self._response.content).get("response")

        def __exit__(self, exc_type, exc_val, exc_tb):
            super().__exit__(exc_type, exc_val, exc_tb)
            self._commandSet._cmd._add_ioc_to_cache(self._params.ioc)
