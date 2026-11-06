from cmd2 import CommandSet, Statement

from sp.commands.base.BaseCommand import BaseCommand
from sp.common.exceptions import CommandError
from sp.settings import API_URL


class BaseSPQL(BaseCommand):
    """
    SPQL main command
    """

    _URL = API_URL + "v1/spql-search?format=json"
    """The SPQL endpoint URL"""
    query: str = ""
    """The SPQL query string i.e.: 'domain=ig.com'"""
    datasource: list = ["webscan"]
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
        self.datasource = params.datasource or self.datasource
        self.fields = params.fields or self.fields
        self.sort = params.sort or self.sort
        self.limit = params.limit or 100
        self.verbose = params.verbose or False
        super().__init__(params, command_set)

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

        :return: The parsed JSON response
        """
        if not self.query:
            raise CommandError("You need to specify a query")
        self.payload = {
            "query": self._get_query(),
            "fields": self.fields,
            "sorting": self.sort,
            "limit": self.limit,
        }
        return self.call_api("POST", self.payload)


class WebScan(BaseSPQL):
    _URL = API_URL + "v1/explore/scandata/search/raw?format=json"
    datasource: list = ["webscan"]
    """The SPQL data source which to query for"""
    sort: list = ["scan_date/desc"]
    """The default sort, first_seen_on is a feed field, not a webscan one"""

    def __enter__(self):
        """
        Overrides BaseCommand.__enter__: the webscan endpoint reads the limit from the URL, not from the payload

        :return: WebScan
        """
        if self._params.limit:
            self._URL += f"&limit={self._params.limit}"
        return super().__enter__()

    def scan(self):
        """
        Overrides BaseSPQL.scan: extracts the webscan results from the response

        :return: None
        """
        self._result = (super().scan().get("response", {}) or {}).get("scandata_raw")


class FeedScan(BaseSPQL):
    _URL = API_URL + "v2/feed-scan/query-data/?format=json"
    datasource: list = ["FEED", "DRAFT"]
    """The SPQL data source which to query for"""

    def scan(self):
        """
        Overrides BaseSPQL.scan: extracts the feed results from the response

        :return: None
        """
        response = super().scan().get("response", {}) or {}
        self._result = response if self.verbose else response.get("data")
