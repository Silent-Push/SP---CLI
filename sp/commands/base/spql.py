import json

import requests
from cmd2 import CommandSet, Statement

from sp.commands.base.BaseCommand import BaseCommand
from sp.settings import API_KEY, API_URL


class BaseSPQL(BaseCommand):
    """
    SPQL main command
    """

    _URL = API_URL + "v1/merge-api/explore/scandata/search/raw?format=json"
    """The SPQL endpoint URL"""
    query: str = ""
    """The SPQL query string i.e.: 'domain=ig.com'"""
    datasource: list = ["webscan"]
    # TODO: fields is accepted in SPQL https://silentpush.atlassian.net/wiki/spaces/TI/pages/1576075279/Example+Web+Scanner+Queries+Other+Search+Tips
    """The SPQL data source which to query for"""
    fields: list = []
    """The output fields parameter"""
    limit: int = 100
    """The number of results to return"""
    verbose: bool = False
    """If should include metadata in results"""
    sort: list = ["first_seen_on/desc"]
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
        if not self.query:
            raise ValueError("need a query!")
        self.datasource = params.datasource or self.datasource
        self.fields = params.fields or self.fields
        self.sort = params.sort or self.sort
        self.limit = params.limit or 100
        self.verbose = params.verbose or False
        super().__init__(params, command_set)

    def __enter__(self):
        self._feedback = "executing query"
        return super().__enter__()

    def _get_query(self):
        """
        Prepares the query string according to the syntax

        :return: The query string
        """
        datasources = ",".join(f'"{d}"' for d in self.datasource)
        if self._commandSet._cmd.interactive or (self.query[0] == "'" and self.query[-1] == "'"):
            self.query = self.query[1:-1]
        return self.query + " AND datasource=[" + datasources + "]"

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
            # "fields": self.fields,  # @TODO: not supported yet
            "sorting": self.sort,
            "limit": self.limit,
        }
        self._response = requests.post(
            self._URL, json=self.payload, headers={"x-api-key": API_KEY}
        )
        self.check_error()


class WebScan(BaseSPQL):
    _URL = API_URL + "v1/merge-api/explore/scandata/search/raw?format=json"
    datasource: list = ["webscan"]
    """The SPQL data source which to query for"""

    def scan(self):
        super().scan()
        self._response = (
                json.loads(self._response.content).get("response", {}) or {}
        ).get("scandata_raw")


class FeedScan(BaseSPQL):
    _URL = API_URL + "v2/feed-scan/query-data/?format=json"
    datasource: list = ["FEED", "DRAFT"]
    """The SPQL data source which to query for"""

    def scan(self):
        super().scan()
        try:
            if self.verbose:
                self._response = json.loads(self._response.content).get("response")
            else:
                self._response = (
                        json.loads(self._response.content).get("response", {}) or {}
                ).get("data")
        except json.JSONDecodeError as e:
            self._commandSet._cmd.perror(f"Can't parse command response: {e.msg}")
