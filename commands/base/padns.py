import json
import requests

from commands.base.BaseCommand import BaseCommand
from settings import CRLF, API_URL, API_KEY


class PADNS(BaseCommand):
    _URL = API_URL + "explore/padns/lookup/{type}/{qtype}/{ioc}/"
    _type: str = "query"
    _qtype: str = "any"
    _feedback: str = ""

    def __init__(
        self,
        params,
        command_set,
        type: str = "query",
        qtype: str = "any",
    ):
        self._type = type
        self._qtype = qtype
        super().__init__(params, command_set)

    def __enter__(self):
        self._URL = self._URL.format(
            type=self._type,
            qtype=self._qtype,
            ioc=self._params.ioc
        )
        if self._params.params:
            self._URL += "?" + "&".join(self._params.params)
        self._feedback = f"{self._URL[self._URL.index('lookup/') + 7:]}"
        self._commandSet._cmd.pfeedback(f"\t{self._feedback}...")
        return self

    def lookup(self):
        response = requests.get(
            self._URL,
            headers={"x-api-key": API_KEY}
        )
        self._response = json.loads(response.content).get("response")

    def __exit__(self, exc_type, exc_val, exc_tb):
        super().__exit__(exc_type, exc_val, exc_tb)
        self._commandSet._cmd.poutput(self._output)
        self._commandSet._cmd.pfeedback(f"\t*{self._feedback}")
        self._commandSet._cmd._add_ioc_to_cache(self._params.ioc)
