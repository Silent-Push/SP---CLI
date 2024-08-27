import json
import requests

from sp.commands.base.BaseCommand import BaseCommand
from sp.settings import API_URL, API_KEY


class SPQL(BaseCommand):
    _URL = API_URL + "explore/scandata/search/raw?format=json"
    query: str = ""
    datasource: str = "webscan"
    fields: list = []
    sort: list = []
    payload: dict = {}
    _feedback: str = ""

    def __init__(
        self,
        params,
        command_set,
    ):
        self.query = params.query
        self.datasource = params.datasource
        self.fields = params.fields
        self.sort = params.sort
        super().__init__(params, command_set)

    def _get_query(self):
        return (
            ''.join(self.query) +
            f" AND datasource={self.datasource or 'webscan'}"
        )

    def scan(self):
        if not self.query:
            self._commandSet._cmd.perror("You need to specify a query")
            return
        self.payload = {
            "query": self._get_query(),
            "fields": self.fields,
            "sort": self.sort,
        }
        self._response = requests.post(
            self._URL, json=self.payload, headers={"x-api-key": API_KEY}
        )
        self.check_error()
        self._response = json.loads(self._response.content).get("response")
