import json
import requests

from sp.commands.base.BaseCommand import BaseCommand
from sp.settings import API_URL, API_KEY


class PADNS(BaseCommand):
    _URL = API_URL + "explore/padns/lookup/{type}/{qtype}/{ioc}/?format=json"
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
            type=self._type, qtype=self._qtype, ioc=self._params.ioc
        )
        super().__enter__()
        self._feedback = f"{self._URL[self._URL.index('lookup/') + 7:]}"
        return self

    def lookup(self):
        if not self._params.ioc:
            self._commandSet._cmd.perror("You need to pass the IoC")
            return
        self._response = requests.get(
            self._URL,
            headers={"x-api-key": API_KEY, "User-Agent": "SP-CLI"},
        )
        self.check_error()
        self._response = json.loads(self._response.content).get("response")

    def __exit__(self, exc_type, exc_val, exc_tb):
        super().__exit__(exc_type, exc_val, exc_tb)
        self._commandSet._cmd._add_ioc_to_cache(self._params.ioc)
