import json
import requests
from cmd2 import Statement, CommandSet

from sp.commands.base.BaseCommand import BaseCommand
from sp.settings import API_URL, API_KEY


class SPQL(BaseCommand):
    """
    SPQL main command
    """
    _URL = API_URL + "explore/scandata/search/raw?format=json"
    """The SPQL endpoint URL"""
    query: str = ""
    """The SPQL query string i.e.: 'domain=ig.com'"""
    datasource: str = "webscan"
    """The SPQL data source which to query for"""
    fields: list = []
    """The output fields parameter"""
    sort: list = []
    """The sort parameter"""
    payload: dict = {}
    """The final payload to post"""

    def __init__(
        self,
        params: Statement,
        command_set: CommandSet,
    ):
        """
        Base class for the SPQL sub commands,
        it's used by the sub commands i.e.: webscan

        :param params: The passed command options
        :param command_set: The CommandSet object related to the command
        """
        self.query = params.query
        self.datasource = params.datasource
        self.fields = params.fields
        self.sort = params.sort
        super().__init__(params, command_set)

    def _get_query(self):
        """
        Prepares the query string according to the syntax

        :return: The query string
        """
        return (
            ''.join(self.query) +
            f" AND datasource={self.datasource or 'webscan'}"
        )

    def scan(self):
        """
        The SPQL main command logic

        :return: None
        """
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
